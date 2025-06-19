import hcl2
import os


def load_hcl(path):
    print("[*] Loading HCL files from path:", path)
    # Walk the path and load all HCL files
    terraform_files = []
    for root, _, files in os.walk(path):
        for fname in files:
            if fname.endswith('.tf'):
                full_path = os.path.join(root, fname)
                print(f"[*] Found Terraform file: {full_path}")
                # Parse the HCL file
                # Use hcl2 to load the file, catching any parsing errors
                with open(full_path, 'r') as f:
                    try:
                        terraform_files.append((full_path, hcl2.load(f)))
                    except hcl2.HCLParseError as e:
                        print(f"[!] Error parsing {full_path}: {e}")
    
    return terraform_files


def extract_resources(terraform_files):
    for file_path, terraform_file in terraform_files:
        print(f"[*] Extracting resources from {file_path}")
        for block in terraform_file.get("resource", []):
            for r_type, instances in block.items():
                for name, attrs in instances.items():
                    # Each instance is a dict of attributes
                    # print(f"[*] Found resource: [r_type: {r_type} | name: {name} | attrs: {attrs}]\n")
                    yield {
                        "file": file_path,
                        "type": r_type,
                        "name": name,
                        "attrs": attrs
                    }
    