from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    """Enumeration for severity levels of findings."""
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Finding:
    """Class representing a finding from a scan."""
    resource_type: str
    resource_name: str
    rule_id: str
    severity: SeverityLevel
    description: str
    location: str
    timestamp: datetime.date
    