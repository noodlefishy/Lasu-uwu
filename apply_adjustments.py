import json
import os
import yaml

# Load adjustments
with open('adjustments.json', 'r') as f:
    adjustments = json.load(f)

for adj in adjustments:
    file_path = adj['file']
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    with open(file_path, 'r') as f:
        content = f.read()

    # Split content into YAML and body
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1]
            body = parts[2]
            
            # Parse YAML
            try:
                data = yaml.safe_load(yaml_content)
                if data is None: data = {}
            except yaml.YAMLError as exc:
                print(f"Error parsing YAML in {file_path}: {exc}")
                continue
            
            # Update fields
            data['pronunciation'] = adj['pronunciation']
            data['sentimental meaning'] = adj['sentimental meaning']
            data['etymology'] = adj['etymology']
            
            # Write back
            new_yaml = yaml.dump(data, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{new_yaml}---\n{body.lstrip()}"
            
            with open(file_path, 'w') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"Malformed YAML in {file_path}")
    else:
        print(f"No YAML header found in {file_path}")
