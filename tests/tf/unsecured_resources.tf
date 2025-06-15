resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-unsecure-public-bucket"
}

resource "aws_security_group" "open_sg" {
  name        = "demo-unsecure-open-sg"
  description = "Allow SSH from anywhere"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}
