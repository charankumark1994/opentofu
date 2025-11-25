terraform {
  required_providers {
    aws = {
      source  = "opentofu/aws"
      version = ">= 5.56.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# Existing S3 bucket
variable "existing_bucket" {
  default = "pykc"
}

resource "aws_s3_object" "demo_object" {
  bucket  = var.existing_bucket
  key     = "workspace-test-${terraform.workspace}/hello.txt"
  content = "This file belongs to workspace: ${terraform.workspace}"
}

output "workspace" {
  value = terraform.workspace
}

output "object_path" {
  value = aws_s3_object.demo_object.key
}
