provider "aws" {
  region = "ap-southeast-2"
}
 
variable "instance_types" {
  type    = list(string)
  default = ["t3.micro", "t3.small"]
}
 
resource "aws_instance" "multi" {
  for_each      = toset(var.instance_types)
  ami           = "ami-0715b650e07377859" # Example AMI
  instance_type = each.key
  tags = {
    Name = "Instance-${each.key}"
  }
}