provider "aws" {
  region = "ap-southeast-2"
}
 
resource "aws_instance" "example" {
  ami           = "ami-0715b650e07377859"
  instance_type = "t3.small"
  #key_name      = "TofuPractise"
 
  tags = {
    Name = "HelloWorld"
  }
}



