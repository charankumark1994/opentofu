ssh -i "my-key.pem" ec2-user@16.176.129.203terraform {
  required_version = ">= 1.7.0"

  required_providers {
    aws = {
      source  = "registry.opentofu.org/hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# Get all EC2 instance IDs in the region
data "aws_instances" "all" {}

# Fetch full details for each EC2 instance
data "aws_instance" "details" {
  for_each    = toset(data.aws_instances.all.ids)
  instance_id = each.value
}

# Output EC2 details
output "ec2_details" {
  value = data.aws_instance.details
}
