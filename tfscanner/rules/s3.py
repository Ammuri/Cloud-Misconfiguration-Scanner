from cloudscanner.common import Finding, SeverityLevel
from datetime import datetime

def check_s3_bucket_legacy_acl(resource):
    findings = []
    
    attrs = resource["attrs"]
    file = resource["file"]
    name = resource["name"]
    
    
    acl = attrs.get("acl")
    if acl in ("public-read", "public-read-write"):
        print(f"Found legacy ACL '{acl}' for S3 bucket '{name}' in file '{file}'")
        findings.append(
            Finding(
                resource_type = resource["type"],
                resource_name = name,
                rule_id = "S3_LEGACY_PUBLIC_ACL",
                severity = SeverityLevel.HIGH,
                description = (
                    f"S3 bucket '{name}' in file '{file}' still uses legacy ACL '{acl}', which is insecure and deprecated. Move to object ownership."
                ),
                location = file,
                timestamp = datetime.now().date()
            )
        )
    elif acl == "private":
        findings.append(
            Finding(
                resource_type = resource["type"],
                resource_name = name,
                rule_id = "S3_LEGACY_PRIVATE_ACL",
                severity = SeverityLevel.LOW,
                description = (
                    f"S3 bucket '{name}' in file '{file}' uses legacy ACL 'private'. Consider using bucket policies instead."
                ),
                location = file,
                timestamp = datetime.now().date()
            )
        )
    
    return findings