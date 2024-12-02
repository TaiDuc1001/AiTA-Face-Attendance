import os
import yaml
import argparse

def convert_to_dict(obj):
    if isinstance(obj, argparse.Namespace): 
        return {k: convert_to_dict(v) for k, v in vars(obj).items()}
    else:
        return obj

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


def get_latest_config():
    config_files = [f for f in os.listdir() if f.endswith('.yaml')]
    if not config_files:
        return None
    return max(config_files, key=os.path.getctime)
