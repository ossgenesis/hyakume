# Container registry — holds the inference + LLM model server images.
resource "azurerm_container_registry" "main" {
  name                = "${var.prefix}${var.environment}acr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false
  tags                = local.tags
}

# Let the AKS kubelet pull images from ACR without credentials.
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.main.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.main.kubelet_identity[0].object_id
}

# Object storage — raw captures (RGB + LiDAR depth), heatmaps, report PDFs.
resource "azurerm_storage_account" "main" {
  name                     = "${var.prefix}${var.environment}st${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = local.tags
}

resource "azurerm_storage_container" "captures" {
  name                  = "captures"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "reports" {
  name                  = "reports"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Metadata DB — org/user/device/scan/slab/defect records.
resource "azurerm_postgresql_flexible_server" "main" {
  name                          = "${local.name}-pg-${random_string.suffix.result}"
  resource_group_name           = azurerm_resource_group.main.name
  location                      = azurerm_resource_group.main.location
  version                       = "16"
  administrator_login           = var.postgres_admin_login
  administrator_password        = var.postgres_admin_password
  sku_name                      = "B_Standard_B1ms"
  storage_mb                    = 32768
  public_network_access_enabled = true # POC convenience; lock down with VNet integration for prod
  zone                          = "1"
  tags                          = local.tags
}

resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "stonescan"
  server_id = azurerm_postgresql_flexible_server.main.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}
