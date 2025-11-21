terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# Fetch all EC2 instances
data "aws_instances" "all" {}

# Fetch full details of each instance
data "aws_instance" "details" {
  for_each = toset(data.aws_instances.all.ids)
  instance_id = each.value
}

# Output the details
output "ec2_details" {
  value = data.aws_instance.details
}
