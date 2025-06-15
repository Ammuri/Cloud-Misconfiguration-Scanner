## scanner.py

import os
import importlib
import pkgutil
import click
from tfscanner import parser
from cloudscanner.aws import AWSScanner
from report.json_report import to_json
from cloudscanner.common import Finding

# Utility: Discover all available Terraform rule functions
def discover_tf_rules():
    """Dynamically import tfscanner.rules modules and list functions starting with 'check_'"""
    rules_pkg = tfscanner.rules
    module_path = rules_pkg.__path__
    for finder, name, ispkg in pkgutil.iter_modules(module_path):
        module = importlib.import_module(f"tfscanner.rules.{name}")
        for attr in dir(module):
            if attr.startswith('check_'):
                yield getattr(module, attr)

@click.group()
def cli():
    """Cloud Misconfiguration Scanner CLI"""
    pass

@cli.command('tf')
@click.argument('path', type=click.Path(exists=True))
@click.option('--rules', default='', help='Comma-separated list of rule names (e.g. check_s3_bucket)')
def tf_scan(path, rules):
    """Static scan of Terraform code at PATH"""
    # Load and parse HCL
    config = parser.load_hcl(path)
    findings = []

    # Determine which rules to run
    available = {func.__name__: func for func in discover_tf_rules()}
    selected = rules.split(',') if rules else list(available.keys())

    for name in selected:
        if name not in available:
            click.echo(f"[!] Rule '{name}' not found. Skipping.")
            continue
        func = available[name]
        # Traverse parsed config for each resource attrs dict
        for block in parser.extract_resources(config):  # implement extract_resources in parser
            findings.extend(func(block))

    click.echo(to_json(findings))

@cli.command('live')
@click.option('--profile', default='default', help='AWS CLI profile name')
@click.option('--region', default='us-east-1', help='AWS region')
def live_scan(profile, region):
    """Live scan of AWS account"""
    scanner = AWSScanner(profile_name=profile, region_name=region)
    findings = []
    findings.extend(scanner.scan_s3())
    findings.extend(scanner.scan_sg())
    click.echo(to_json(findings))

if __name__ == '__main__':
    cli()
 
