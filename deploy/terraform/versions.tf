terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # For team use, store state remotely instead of locally. Create the storage
  # account/container once, then uncomment and `terraform init -migrate-state`.
  # backend "azurerm" {
  #   resource_group_name  = "stonescan-tfstate"
  #   storage_account_name = "stonescantfstate"
  #   container_name       = "tfstate"
  #   key                  = "poc.terraform.tfstate"
  # }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

provider "random" {}
