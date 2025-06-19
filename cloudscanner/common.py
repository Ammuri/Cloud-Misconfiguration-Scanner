from dataclasses import dataclass
from datetime import datetime


@dataclass
class Finding:
    """Class representing a finding from a scan."""
    resrouce_type: str
    resource_name: str
    rule_id: str
    severity: str
    description: str
    location: str
    timestamp: datetime
    
    
