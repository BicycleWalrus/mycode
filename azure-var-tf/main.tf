terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.23.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.name
  location = var.loc
}

variable "loc" {
  type    = string
  default = "westus2"
}

variable "name" {
  type    = string
  default = "rg-1"
}
