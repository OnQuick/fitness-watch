output "function_app_name" {
    value = azurerm_linux_function_app.function_app.name
}

output "function_app_url" {
    value = "https://${azurerm_linux_function_app.function_app.default_hostname}"
}

output "iot_hub_name" {
    value = azurerm_iothub.iothub.name
}

output "iot_hub_connection_string" {
    value = azurerm_iothub_shared_access_policy.policy.primary_connection_string
    sensitive = true
}

output "cosmos_db_account_name" {
    value = azurerm_cosmosdb_account.cosmos.name
}

output "cosmos_db_database_name" {
    value = azurerm_cosmosdb_sql_database.database.name
}

output "cosmos_db_container_name" {
    value = azurerm_cosmosdb_sql_container.container.name
} 