import os
import sys
# Add project root (two levels up) to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tfscanner.parser import load_hcl, extract_resources

# Directory containing our .tf fixtures
test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tf'))

def test_load_hcl_returns_list_of_tuples():
    terraform_files = load_hcl(test_dir)
    assert isinstance(terraform_files, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in terraform_files)

def test_extract_resources_yields_expected_structure():
    terraform_files = load_hcl(test_dir)
    resources = list(extract_resources(terraform_files))
    assert all(isinstance(res, dict) for res in resources)
    # Each resource dict should have these keys
    for res in resources:
        assert set(res.keys()) >= {"file", "type", "name", "attrs"}
    # Check that at least one S3 bucket and correct file path appear
    assert any(r["type"] == "aws_s3_bucket" for r in resources)
    assert any(r["file"].endswith("unsecured_resources.tf") for r in resources)