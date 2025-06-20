import json
from dataclasses import asdict

def to_json(findings):
    """Convert findings to JSON format."""
    return json.dumps([asdict(finding) for finding in findings], indent=2, default=str)