import os
import json
import shutil

def extract_digests(root_path, model, version):
    # Expand tilde to full home directory path
    root_path = os.path.expanduser(root_path)
    # Construct the path to the version file
    file_path = os.path.join(root_path, "manifests", "registry.ollama.ai", "library", model, version)
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    
    # Check if it's a file
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a file.")
        return None
    
    # Read and parse the JSON file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON in '{file_path}': {e}")
        return None
    except OSError as e:
        print(f"Error: Unable to read file '{file_path}': {e}")
        return None
    
    # Extract all digest values recursively
    digests = []
    def find_digests(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "digest":
                    digests.append(value)
                else:
                    find_digests(value)
        elif isinstance(obj, list):
            for item in obj:
                find_digests(item)
    
    find_digests(data)
    return digests

def copy_blobs(root_path, destination_root, digests):
    # Paths for source and destination blobs
    src_blobs = os.path.join(os.path.expanduser(root_path), "blobs")
    dest_blobs = os.path.join(os.path.expanduser(destination_root), "blobs")
    
    # Create destination blobs directory if it doesn't exist
    os.makedirs(dest_blobs, exist_ok=True)
    
    # Copy each blob file
    for digest in digests:
        # Replace 'sha256:' with 'sha256-' to match file naming convention
        file_name = digest.replace("sha256:", "sha256-")
        src_file = os.path.join(src_blobs, file_name)
        dest_file = os.path.join(dest_blobs, file_name)
        
        if os.path.exists(src_file):
            try:
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {file_name} to {dest_blobs}")
            except OSError as e:
                print(f"Error: Failed to copy '{src_file}' to '{dest_file}': {e}")
        else:
            print(f"Warning: Source file '{src_file}' does not exist.")

def copy_version_and_create_model_folder(root_path, destination_root, model, version):
    # Source and destination paths
    root_path = os.path.expanduser(root_path)
    destination_root = os.path.expanduser(destination_root)
    src_model_dir = os.path.join(root_path, "manifests", "registry.ollama.ai", "library", model)
    dest_model_dir = os.path.join(destination_root, "manifests", "registry.ollama.ai", "library", model)
    
    # Create the destination manifests/registry.ollama.ai/library/<model> directory if it doesn't exist
    os.makedirs(dest_model_dir, exist_ok=True)
    
    # Copy the specified version file
    src_version = os.path.join(src_model_dir, version)
    dest_version = os.path.join(dest_model_dir, version)
    
    if os.path.exists(src_version):
        try:
            shutil.copy2(src_version, dest_version)
            print(f"Copied: '{version}' file to {dest_model_dir}")
        except OSError as e:
            print(f"Error: Failed to copy '{version}' file to '{dest_version}': {e}")
    else:
        print(f"Warning: '{version}' file not found in {src_model_dir}")

def main():
    # Get root and destination_root once
    root = input("Enter the root path of the Ollama models folder: ").strip()
    destination_root = input("Enter the destination root path of the Ollama model folder: ").strip()
    
    while True:
        # Ask for model and version
        model = input("\nEnter the name of the model (or 'exit' to quit): ").strip()
        if model.lower() == 'exit':
            print("Exiting program.")
            break
        
        version = input("Enter the version of the model: ").strip()
        
        # Step 1: Extract digests
        digests = extract_digests(root, model, version)
        
        if digests is not None:
            # Print digests
            if digests:
                print(f"\nDigest values found in {root}/manifests/registry.ollama.ai/library/{model}/{version}:")
                for digest in digests:
                    print(f"  {digest}")
            else:
                print(f"\nNo 'digest' keys found in the JSON file.")
                continue
            
            # Step 2: Copy blobs
            copy_blobs(root, destination_root, digests)
            
            # Step 3: Create model folder and copy the version file
            copy_version_and_create_model_folder(root, destination_root, model, version)
        
        # Ask if the user wants to continue
        continue_choice = input("\nDo you want to process another model? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()