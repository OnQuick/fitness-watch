terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  suffix = random_id.suffix.hex
}

resource "azurerm_resource_group" "iot_rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_iothub" "iothub" {
  name                = "${var.iot_hub_name}${local.suffix}"
  resource_group_name = azurerm_resource_group.iot_rg.name
  location            = azurerm_resource_group.iot_rg.location

  sku {
    name     = "F1"
    capacity = 1
  }

  tags = {
    purpose = "telemetry"
  }
}

resource "azurerm_iothub_shared_access_policy" "policy" {
  name                = "terraform-policy"
  resource_group_name = azurerm_resource_group.iot_rg.name
  iothub_name         = azurerm_iothub.iothub.name

  registry_read   = true
  registry_write  = true
  service_connect = true
  device_connect  = true
}

# Cosmos DB Account
resource "azurerm_cosmosdb_account" "cosmos" {
  name                = "${var.cosmos_db_account_name}${local.suffix}"
  location            = azurerm_resource_group.iot_rg.location
  resource_group_name = azurerm_resource_group.iot_rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  automatic_failover_enabled = false

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.iot_rg.location
    failover_priority = 0
  }

  tags = {
    purpose = "telemetry-storage"
  }
}

# Cosmos DB Database
resource "azurerm_cosmosdb_sql_database" "database" {
  name                = var.cosmos_db_database_name
  resource_group_name = azurerm_cosmosdb_account.cosmos.resource_group_name
  account_name        = azurerm_cosmosdb_account.cosmos.name
}

# Cosmos DB Container
resource "azurerm_cosmosdb_sql_container" "container" {
  name                  = var.cosmos_db_container_name
  resource_group_name   = azurerm_cosmosdb_account.cosmos.resource_group_name
  account_name          = azurerm_cosmosdb_account.cosmos.name
  database_name         = azurerm_cosmosdb_sql_database.database.name
  partition_key_paths   = ["/deviceId"]
  partition_key_version = 1

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    excluded_path {
      path = "/\"_etag\"/?"
    }
  }
}

# Stream Analytics Job
resource "azurerm_stream_analytics_job" "stream_analytics" {
  name                                     = "${var.stream_analytics_job_name}${local.suffix}"
  resource_group_name                      = azurerm_resource_group.iot_rg.name
  location                                 = azurerm_resource_group.iot_rg.location
  compatibility_level                      = "1.2"
  data_locale                             = "en-US"
  events_late_arrival_max_delay_in_seconds = 60
  events_out_of_order_max_delay_in_seconds = 50
  events_out_of_order_policy              = "Adjust"
  output_error_policy                     = "Drop"
  streaming_units                         = 1

  transformation_query = <<QUERY
    SELECT
        deviceId,
        steps,
        heart_rate,
        EventEnqueuedUtcTime as timestamp,
        CONCAT(deviceId, '_', CAST(EventEnqueuedUtcTime AS nvarchar(max))) as documentId
    INTO [cosmos-output]
    FROM [iothub-input]
    WHERE deviceId IS NOT NULL
QUERY

  tags = {
    purpose = "telemetry-processing"
  }
}

# Stream Analytics Input - IoT Hub
resource "azurerm_stream_analytics_stream_input_iothub" "iothub_input" {
  name                         = "iothub-input"
  stream_analytics_job_name    = azurerm_stream_analytics_job.stream_analytics.name
  resource_group_name          = azurerm_resource_group.iot_rg.name
  endpoint                     = "messages/events"
  shared_access_policy_name    = "terraform-policy"
  shared_access_policy_key     = azurerm_iothub_shared_access_policy.policy.primary_key
  iothub_namespace             = azurerm_iothub.iothub.name
  eventhub_consumer_group_name = "$Default"

  serialization {
    type     = "Json"
    encoding = "UTF8"
  }
}

# Stream Analytics Output - Cosmos DB
resource "azurerm_stream_analytics_output_cosmosdb" "cosmos_output" {
  name                     = "cosmos-output"
  stream_analytics_job_id  = azurerm_stream_analytics_job.stream_analytics.id
  cosmosdb_account_key     = azurerm_cosmosdb_account.cosmos.primary_key
  cosmosdb_sql_database_id = azurerm_cosmosdb_sql_database.database.id
  container_name           = azurerm_cosmosdb_sql_container.container.name
  document_id              = "documentId"
  partition_key            = "deviceId"
}
