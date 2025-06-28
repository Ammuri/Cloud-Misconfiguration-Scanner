import boto3
from cloudscanner.common import Finding, SeverityLevel
from datetime import datetime

class AWSScanner:
    def __init__(self, profile_name, region_name):
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        self.iam=session.client("iam")
        
    def scan_root_mfa(self):
        findings = []
        summary = self.iam.get_account_summary().get("SummaryMap", {})
        
        if summary.get("AccountMFAEnabled") == 0:
            findings.append(
                Finding(
                    resource_type="aws_iam_user",
                    resource_name="root",
                    rule_id="ROOT_NO_MFA",
                    severity=SeverityLevel.CRITICAL,
                    description="Root account has no MFA. This is a critical security risk. It is recommended to enable MFA for the root account.",
                    location="aws:iam/root",
                    timestamp=datetime.now().date()
                )
            )
        
        return findings
