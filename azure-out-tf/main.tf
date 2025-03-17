terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "myTFResourceGroup"
  location = var.loc
}

variable "loc" {
  type    = string
  default = "westus2"
}

output "rg_id" {
  value       = azurerm_resource_group.rg.id
  description = "ID of the resource group"
}
