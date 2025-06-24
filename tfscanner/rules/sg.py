from datetime import datetime
from cloudscanner.common import Finding, SeverityLevel

def check_sg_open_ingress(resource):
    findings = []
    attrs = resource["attrs"]
    file = resource["file"]
    name = resource["name"]
    
    if "ingress" in attrs:
        for rule in attrs["ingress"]:
            if "cidr_blocks" in rule and (
                "0.0.0.0/0" in rule["cidr_blocks"] 
                or "::/0" in rule["cidr_blocks"]
            ):
                print(f"Found open ingress rule for security group '{name}' in file '{file}'")
                findings.append(
                    Finding(
                        resource_type=resource["type"],
                        resource_name=name,
                        rule_id="SG_OPEN_INGRESS",
                        severity=SeverityLevel.HIGH,
                        description=(
                            f"Security group '{name}' in file '{file}' allows ingress from all IPs."
                        ),
                        location=file,
                        timestamp=datetime.now().date()
                    )
                )
            
            if "protocol" in rule and rule["protocol"] == "-1":
                print(f"Found 'any' protocol rule for security group '{name}' in file ' {file}'")
                findings.append(
                    Finding(
                        resource_type=resource["type"],
                        resource_name=name,
                        rule_id="SG_ANY_PROTOCOL",
                        severity=SeverityLevel.MEDIUM,
                        description=(
                            f"Security group '{name}' in file '{file}' allows ingress with 'any' protocol."
                        ),
                        location=file,
                        timestamp=datetime.now().date()
                    )
                )
    if resource["type"] == "aws_vpc_security_group_ingres_rule":
        # Handle the case where the ingress rule is defined in a separate resource
        if attrs.get("ip_protocol") == "-1":
            print(f"Found 'any' protocol rule for security group '{name}' in file '{file}'")
            findings.append(
                Finding(
                    resource_type=resource["type"],
                    resource_name=name,
                    rule_id="SG_ANY_PROTOCOL",
                    severity=SeverityLevel.MEDIUM,
                    description=(
                        f"Security group '{name}' in file '{file}' allows ingress with 'any' protocol."
                    ),
                    location=file,
                    timestamp=datetime.now().date()
                )
            )
    
    return findings

def check_sg_open_egress(resource):
    findings = []
    attrs = resource["attrs"]
    file = resource["file"]
    name = resource["name"]
    
    if "egress" in attrs:
        for rule in attrs["egress"]:
            if "cidr_blocks" in rule and (
                "0.0.0.0/0" in rule["cidr_blocks"] 
                or "::/0" in rule["cidr_blocks"]
            ):
                print(f"Found open egress rule for security group '{name}' in file '{file}'")
                findings.append(
                    Finding(
                        resource_type=resource["type"],
                        resource_name=name,
                        rule_id="SG_OPEN_EGRESS",
                        severity=SeverityLevel.MEDIUM,
                        description=(
                            f"Security group '{name}' in file '{file}' allows egress to all IPs."
                        ),
                        location=file,
                        timestamp=datetime.now().date()
                    )
                )
            elif "protocol" in rule and rule["protocol"] == "-1":
                print(f"Found 'any' protocol rule for security group '{name}' in file '{file}'")
                findings.append(
                    Finding(
                        resource_type=resource["type"],
                        resource_name=name,
                        rule_id="SG_ANY_PROTOCOL",
                        severity=SeverityLevel.MEDIUM,
                        description=(
                            f"Security group '{name}' in file '{file}' allows egress with 'any' protocol."
                        ),
                        location=file,
                        timestamp=datetime.now().date()
                    )
                )
    elif resource["type"] == "aws_vpc_security_group_egress_rule":
        # Handle the case where the egress rule is defined in a separate resource
        if attrs.get("cidr_ipv4") == "0.0.0.0/0" or attrs.get("cidr_ipv4") == "::/0":
            print(f"Found open egress rule for security group '{name}' in file '{file}'")
            findings.append(
                Finding(
                    resource_type=resource["type"],
                    resource_name=name,
                    rule_id="SG_OPEN_EGRESS",
                    severity=SeverityLevel.MEDIUM,
                    description=(
                        f"Security group '{name}' in file '{file}' allows egress to all IPs."
                    ),
                    location=file,
                    timestamp=datetime.now().date()
                )
            )
        if attrs.get("ip_protocol") == "-1":
            print(f"Found 'any' protocol rule for security group '{name}' in file '{file}'")
            findings.append(
                Finding(
                    resource_type=resource["type"],
                    resource_name=name,
                    rule_id="SG_ANY_PROTOCOL",
                    severity=SeverityLevel.MEDIUM,
                    description=(
                        f"Security group '{name}' in file '{file}' allows egress with 'any' protocol."
                    ),
                    location=file,
                    timestamp=datetime.now().date()
                )
            )
    return findings