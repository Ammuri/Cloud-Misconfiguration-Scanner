from cloudscanner.common import Finding

def check_s3_bucket_legacy_acl(resource):
    findings = []
    
    attrs = resource["attrs"]
    file = resource["file"]
    name = resource["name"]
    
    #TODO