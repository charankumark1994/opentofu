provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "OpenTofu Migration Lab"
      Owner       = var.owner
    }
  }
}
