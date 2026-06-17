variable "subscription_id" {
  type        = string
  description = "Azure subscription ID to deploy into."
}

variable "prefix" {
  type        = string
  description = "Short name prefix for all resources."
  default     = "stonescan"
}

variable "environment" {
  type        = string
  description = "Environment tag (poc, staging, prod)."
  default     = "poc"
}

variable "location" {
  type        = string
  description = "Azure region. Must have NVadsA10_v5 capacity; eastus / westeurope / southcentralus are safe bets."
  default     = "eastus"
}

variable "kubernetes_version" {
  type        = string
  description = "AKS version. null = let Azure pick the default (recommended for POC)."
  default     = null
}

# ---------- System (CPU) pool: always-on, cheap, runs API/dashboard/system pods ----------

variable "system_vm_size" {
  type        = string
  description = "VM size for the always-on system pool."
  default     = "Standard_D4s_v5"
}

variable "system_min_count" {
  type    = number
  default = 1
}

variable "system_max_count" {
  type    = number
  default = 3
}

# ---------- GPU pools (A10 / NVadsA10_v5) ----------

variable "gpu_vm_size" {
  type        = string
  description = "GPU VM size. Standard_NV36ads_A10_v5 = full A10 (24GB). Standard_NV6ads_A10_v5 = 1/6 A10 (4GB, cheap warm node)."
  default     = "Standard_NV36ads_A10_v5"
}

variable "gpu_warm_min_count" {
  type        = number
  description = "Min nodes in the warm GPU pool. 0 = scale fully to zero (cold starts). Set to 1 during business hours to keep inference warm."
  default     = 0
}

variable "gpu_warm_max_count" {
  type    = number
  default = 2
}

variable "gpu_spot_max_count" {
  type        = number
  description = "Max nodes in the spot GPU pool (experiments / batch). Always scales to zero when idle."
  default     = 2
}

# ---------- Reserved capacity (kept as an option, off by default) ----------

variable "enable_capacity_reservation" {
  type        = string
  description = "When true, pre-books GPU capacity so the warm pool is guaranteed to find a node. Costs money even when idle."
  default     = false
}

variable "capacity_reservation_count" {
  type        = number
  description = "Number of GPU VMs to reserve."
  default     = 1
}

variable "capacity_reservation_zone" {
  type        = string
  description = "Availability zone for the reservation (must match where the warm pool runs)."
  default     = "1"
}

# ---------- Data platform ----------

variable "postgres_admin_login" {
  type    = string
  default = "stonescan_admin"
}

variable "postgres_admin_password" {
  type        = string
  description = "Postgres admin password. Pass via TF_VAR_postgres_admin_password or a tfvars file kept out of git."
  sensitive   = true
}

variable "tags" {
  type = map(string)
  default = {
    project = "stonescan"
    managed = "terraform"
  }
}
