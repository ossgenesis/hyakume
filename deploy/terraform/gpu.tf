# Optional pre-booked GPU capacity. Off by default. When Azure GPU availability
# is tight, flip enable_capacity_reservation = true to guarantee the warm pool
# can always get a node (you pay for the reservation whether used or not).
resource "azurerm_capacity_reservation_group" "gpu" {
  count               = var.enable_capacity_reservation ? 1 : 0
  name                = "${local.name}-gpu-crg"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  zones               = [var.capacity_reservation_zone]
  tags                = local.tags
}

resource "azurerm_capacity_reservation" "gpu" {
  count                         = var.enable_capacity_reservation ? 1 : 0
  name                          = "${local.name}-gpu-cr"
  capacity_reservation_group_id = azurerm_capacity_reservation_group.gpu[0].id
  zone                          = var.capacity_reservation_zone

  sku {
    name     = var.gpu_vm_size
    capacity = var.capacity_reservation_count
  }
}

# Warm GPU pool — serves production inference. Set gpu_warm_min_count = 1 during
# business hours for sub-second responses; 0 off-hours to scale fully to zero.
resource "azurerm_kubernetes_cluster_node_pool" "gpu_warm" {
  name                  = "gpuwarm"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.gpu_vm_size
  mode                  = "User"
  auto_scaling_enabled  = true
  min_count             = var.gpu_warm_min_count
  max_count             = var.gpu_warm_max_count

  capacity_reservation_group_id = var.enable_capacity_reservation ? azurerm_capacity_reservation_group.gpu[0].id : null

  node_labels = {
    "workload" = "inference"
    "gpu"      = "a10"
  }
  node_taints = ["nvidia.com/gpu=true:NoSchedule"]
  tags        = local.tags
}

# Spot GPU pool — cheap, interruptible. For experiments, batch retraining, and
# the in-cluster LLM. Always scales to zero when idle.
resource "azurerm_kubernetes_cluster_node_pool" "gpu_spot" {
  name                  = "gpuspot"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = var.gpu_vm_size
  mode                  = "User"
  priority              = "Spot"
  eviction_policy       = "Delete"
  spot_max_price        = -1 # -1 = pay up to the on-demand price, never evicted on price
  auto_scaling_enabled  = true
  min_count             = 0
  max_count             = var.gpu_spot_max_count

  node_labels = {
    "workload"                              = "experiment"
    "gpu"                                   = "a10"
    "kubernetes.azure.com/scalesetpriority" = "spot"
  }
  node_taints = [
    "nvidia.com/gpu=true:NoSchedule",
    "kubernetes.azure.com/scalesetpriority=spot:NoSchedule",
  ]
  tags = local.tags
}
