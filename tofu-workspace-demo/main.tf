terraform {
  required_providers {
    random = {
      source = "opentofu/random"
      version = ">= 3.6.2"
    }
  }
}

provider "random" {}

resource "random_string" "demo" {
  length  = 8
  special = false
}

output "workspace_name" {
  value = terraform.workspace
}

output "generated_string" {
  value = random_string.demo.result
}
