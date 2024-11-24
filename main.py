import argparse
import yaml
from config import BaseConfig
import subprocess
import os

def parse_args():
    parser = argparse.ArgumentParser(description='AiTA Attendance Checking System with Weaviate and InsightFace')
    parser.add_argument('--mode', type=str, help='Mode to run the system (prepare database or inference)')
    parser.add_argument('--config', type=str, help='Path to configuration file')

    # Vector Database
    parser.add_argument('--host', type=str, help='Weaviate host')
    parser.add_argument('--port', type=int, help='Weaviate port')
    parser.add_argument('--location', type=str, help='Weaviate location directory to store data')

    # Image Database
    parser.add_argument('--dataset', type=str, help='Dataset basename')
    parser.add_argument('--dataset-path', type=str, help='Dataset path (with basename)')

    # Face Recognizer
    parser.add_argument('--recognizer-name', type=str, help='Recognizer name')
    parser.add_argument('--recognizer-path', type=str, help='Path to model weights')

    # Face Detector
    parser.add_argument('--detector-name', type=str, help='Detector name')
    parser.add_argument('--detector-path', type=str, help='Path to detector weights')

    return parser.parse_args()

def update_config():
    args = parse_args()
    config_path = args.config
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    config['mode'] = args.mode

    args = BaseConfig(args.__dict__)
    if args.host is not None:
        config['VectorDatabase']['host'] = args.host
    if args.port is not None:
        config['VectorDatabase']['port'] = args.port
    if args.location is not None:
        config['VectorDatabase']['persistence_data_path'] = args.location

    assert args.dataset in config['ImageDatabase']['names'], 'Dataset not found in configuration'
    config['ImageDatabase']['name'] = args.dataset
    if args.dataset_path is not None:
        config['ImageDatabase'][args.dataset] = args.dataset_path

    assert args.recognizer_name in config['Recognizer']['names'], 'Recognizer not found in configuration'
    config['Recognizer']['name'] = args.recognizer_name
    if args.recognizer_path is not None:
        config['Recognizer'][args.recognizer_name] = args.recognizer_path

    assert args.detector_name in config['Detector']['names'], 'Detector not found in configuration'
    config['Detector']['name'] = args.detector_name
    if args.detector_path is not None:
        config['Detector'][args.detector_name] = args.detector_path

    return config

def preparation():
    cmd = ['python', 'function/preparation.py', '--config', 'temp_config.yaml']
    subprocess.run(cmd)

def inference():
    cmd = ['python', 'function/inference.py', '--config', 'temp_config.yaml']
    subprocess.run(cmd)

def main():
    config = update_config()
    mode = config['mode']
    assert mode in ['preparation', 'inference'], 'Invalid mode, please choose between \'preparation\' or \'inference\''

    with open('temp_config.yaml', 'w') as file:
        yaml.dump(config, file)

    if mode == 'preparation':
        preparation()

    elif mode == 'inference':
        inference()

    os.remove('temp_config.yaml')

if __name__ == '__main__':
    main()