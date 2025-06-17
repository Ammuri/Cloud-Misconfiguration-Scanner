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
                        
    # Merge all loaded HCL files into a single dictionary
    # config = {}
    # for file in terraform_files:
    #     for block_type, block_list in file.items():
    #         #each block_list is a list of dicts
    #         config.setdefault(block_type, []).extend(block_list)
    
    print("The terraform_files contains the following: ", terraform_files)
    return terraform_files


def extract_resources(config):