from cloudscanner.common import Finding, SeverityLevel
from datetime import datetime
import json

def check_overprivileged_iam_policy(resource):
    findings = []
    
    attrs = resource["attrs"]
    file = resource["file"]
    name = resource["name"]
    
    # Try to get the policy JSON string from the resource attributes
    policy_str = attrs.get("policy", None)
    policy_dict = {}

    if policy_str:
        try:
            policy_dict = json.loads(policy_str)
        except (TypeError, json.JSONDecodeError):
            policy_dict = {}
    else:
        # Check if the policy is referenced from a data module (e.g., data.aws_iam_policy_document)
        # Terraform references are often stored as dicts or objects in attrs
        # Try to get the resolved policy from a known attribute
        referenced_policy = attrs.get("statement", None)
        print(f"Referenced policy: {referenced_policy}")
        if referenced_policy and isinstance(referenced_policy, dict):
            policy_dict = referenced_policy
        else:
            # Try to get from other common keys if present
            for key in ["document", "json", "policy_json"]:
                if key in attrs and isinstance(attrs[key], dict):
                    policy_dict = attrs[key]
                    break

    policy = policy_dict.get("Statement", [])
    if not policy:
        return findings
    
    for statement in policy:
        if statement.get("Effect") == "Allow" \
            and statement.get("Action") == ("*" or "[*]") \
            and statement.get("Resource") == ("*" or "[*]"):
                findings.append(
                    Finding(
                        resource_type=resource["type"],
                        resource_name=name,
                        rule_id="IAM_OVERLY_PERMISSIVE_POLICY",
                        severity=SeverityLevel.HIGH,
                        description=(
                            f"IAM policy '{name}' in file '{file}' grants full access to all AWS resources. "
                            "This is overly permissive and should be restricted to specific actions and resources."
                        ),
                        location=file,
                        timestamp=datetime.now().date()
                    )
                )
        
    return findings