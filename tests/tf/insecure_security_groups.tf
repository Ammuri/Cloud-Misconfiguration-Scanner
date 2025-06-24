# The use of inline ingress and egress rules is not recommended by terraform
# and should be avoided.
# Terraform recommends using the aws_vpc_security_group_ingress_rule and aws_vpc_security_group_egress_rule
# resources to manage security group rules.

# Testing insescure inline ingress and egress rules
resource "aws_security_group" "insecure_security_group" {
  name        = "test-insecure-open-sg"
  description = "Allow SSH from anywhere"
  vpc_id = aws_vpc.test_vpc.id
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

# Testing insecure inline ingress rules
resource "aws_security_group" "insecure_ingress_ security_group" {
  name        = "test-insecure-open-ingress-sg"
  description = "Allow SSH from anywhere"
  vpc_id = aws_vpc.test_vpc.id
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["198.162.1.0/16"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

# Testing insecure inline egress rules
resource "aws_security_group" "insecure_egress_security_group" {
    name        = "test-insecure-open-egress-sg"
    description = "Open egress ports and protocols"
    vpc_id = aws_vpc.test_vpc.id
    ingress {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["192.168.1.9/16"]
    }
    egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["::/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
}



# ------------------ These security groups will have security groups using the aws_security_group_ingress/egress_rule resources

resource "aws_security_group" "test_security_group_no_inline_rules" {
  name        = "test-security-group-no-inline-rules"
  description = "This security group has no inline rules"
  vpc_id      = aws_vpc.test_vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "allow_all_ports_ipv4" {
  security_group_id = aws_security_group.test_security_group_no_inline_rules.id
  cidr_ipv4         = aws_vpc.test_vpc.cidr_block
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.test_security_group_no_inline_rules.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}