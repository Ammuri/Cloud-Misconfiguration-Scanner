resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-unsecure-public-bucket"

  // Intentionally adding a public bucket policy - ACL
  // ACLs are deprecated but the scanner logic will look for them and flag as insecure
  acl = "public-read"
}

resource "aws_s3_bucket" "public_bucket_no_acl" {
  bucket = "demo-unsecure-public-bucket-no-acl"

  // Intentionally adding a public bucket policy - ACL
  // ACLs are deprecated but the scanner logic will look for them and flag as deprecated
  // but not insecure
  acl = "private"
}

