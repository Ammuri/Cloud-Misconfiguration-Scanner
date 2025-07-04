resource "aws_iam_policy" "overly_permissive_policy" {
  name        = "overly-permissive-policy"
  path        = "/"
  description = "For testing purposes only, this policy grants full access to all AWS resources."

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "overly_permissive_policy" {
  statement {
    actions   = ["*"]
    resources = ["*"]
    effect = "Allow"
  }
}


resource "aws_iam_policy" "overly_permissive_policy_2" {
    name        = "overly-permissive-policy"
    description = "For testing purposes only, this policy grants full access to all AWS resources."
    policy = data.aws_iam_policy_document.overly_permissive_policy.json
}