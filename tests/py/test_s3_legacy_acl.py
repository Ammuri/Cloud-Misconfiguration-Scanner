import os
import sys
from tfscanner.rules.s3 import check_s3_bucket_legacy_acl
from tfscanner.parser import load_hcl, extract_resources

# Add project root (two levels up) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))



# Directory containing our .tf fixtures
test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tf'))


#Test module for check_s3_bucket_legacy_acl
def test_check_s3_bucket_legacy_acl():
    terraform_files = load_hcl(test_dir)
    resources = list(extract_resources(terraform_files))
    findings = []
    for resource in resources:
        # Check if the resource is an S3 bucket
        if resource["type"] == "aws_s3_bucket":
            findings.extend(check_s3_bucket_legacy_acl(resource))
    
    # Assert we found the expected finding
    assert len(findings) == 1
    assert findings[0].rule_id == "S3_LEGACY_PUBLIC_ACL"
    assert findings[0].location.endswith("unsecured_resources.tf")
