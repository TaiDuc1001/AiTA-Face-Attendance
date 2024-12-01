import os
import yaml

def load_yaml(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def save_config_to_yaml(config, output_path):
    father_dir = os.path.dirname(output_path)
    if not os.path.exists(father_dir):
        os.makedirs(father_dir)

    with open(output_path, 'w') as file:
        yaml.dump(config, file, sort_keys=False)
    print(f'New configuration saved to {output_path}')

def update_config(config, args):
    for key, value in vars(args).items():
        if value is not None:
            keys = key.split('.')
            sub_config = config
            for part in keys[:-1]:
                sub_config = sub_config.get(part, {})
            sub_config[keys[-1]] = value

def get_latest_config():
    config_files = [f for f in os.listdir() if f.endswith('.yaml')]
    if not config_files:
        return None
    return max(config_files, key=os.path.getctime)
