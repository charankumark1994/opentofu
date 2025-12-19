terraform {
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

resource "aws_instance" "my_ec2" {
  ami           = "ami-0e0e7b8c8f7a8c3c9"   # Amazon Linux 2023 in ap-south-1
  instance_type = "t3.micro"

  tags = {
    Name = "MyTofuEC2"
  }
}
