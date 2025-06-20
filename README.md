# Cloud Misconfiguration Scanner
Python-based CLI tool that inspects both live cloud (AWS then Azure) and Terraform code for common security misconfigurations, then outputs a consolidated report (JSON or HTML)

- **Scan for Security Issues:** Inspects both live cloud environments (starting with AWS, then Azure) and Terraform (TF) code for common security misconfigurations.
- **Multi-Source Analysis:** Analyzes both infrastructure-as-code (Terraform files) and actual deployed cloud resources, providing a more comprehensive security assessment.
- **Reporting:** Outputs a consolidated report of findings, currently supporting JSON or HTML formats via the command line interface (CLI).
- **Future Plans:** Intends to expand reporting to a webpage or dashboard, making it easier to visualize and track misconfigurations over time.

# How to Run
## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- (Not-needed) AWS CLI configured with appropriate permissions
- (Not-needed) Azure CLI configured with appropriate permissions (if Azure scanning is enabled)
## Installation
Clone the repository:
   ```bash
   git clone
   ```
## Usage
1.  Navigate to the project directory:
    ```bash
    cd cloud-misconfiguration-scanner
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the scanner (only Terraform scanning (AWS) is currently implemented):
    ```bash
    python scanner.py tf tests/tf
    ```