variable "resource_group_name" {
  description = "Name of the resource group"
  default     = "iot-terraform-rg"
}

variable "location" {
  description = "Azure region"
  default     = "uksouth"
}

variable "iot_hub_name" {
  description = "Base name of the IoT Hub (suffix will be added)"
  default     = "tf-iot"
}

variable "stream_analytics_job_name" {
  description = "Base name of the Stream Analytics job (suffix will be added)"
  default     = "tf-stream-analytics"
}

variable "cosmos_db_account_name" {
  description = "Base name of the Cosmos DB account (suffix will be added)"
  default     = "tf-cosmos"
}

variable "cosmos_db_database_name" {
  description = "Name of the Cosmos DB database"
  default     = "fitness-data"
}

variable "cosmos_db_container_name" {
  description = "Name of the Cosmos DB container"
  default     = "telemetry"
}

