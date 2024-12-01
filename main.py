from utils import load_yaml, update_config, save_config_to_yaml, get_latest_config
import argparse
import subprocess
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description='AiTA Attendance Checking System with Weaviate and InsightFace')
    # General arguments
    parser.add_argument('--General.mode', type=str, help="Mode of operation (preparation/inference)", required=True)
    parser.add_argument('--General.config', type=str, help="Path to configuration file", default='config.yaml')
    parser.add_argument('--General.load-samples', action='store_true', help="Load default samples")
    parser.add_argument('--General.temp-dir', type=str, help="Temporary configs directory", default='configs')

    # Camera arguments
    parser.add_argument('--Camera.name', type=str, help="Camera name")
    parser.add_argument('--Camera.url', type=str, help="Input URL")

    # Detector arguments
    parser.add_argument('--Detector.name', type=str, help="Detector name")
    parser.add_argument('--Detector.path', type=str, help="Path for detector")

    # Recognizer arguments
    parser.add_argument('--Recognizer.name', type=str, help="Recognizer name")

    # NoSQLDatabase arguments
    parser.add_argument('--NoSQLDatabase.name', type=str, help="NoSQL database name")
    parser.add_argument('--NoSQLDatabase.hostname', type=str, help="NoSQL hostname")
    parser.add_argument('--NoSQLDatabase.port', type=int, help="NoSQL port")
    parser.add_argument('--NoSQLDatabase.persistence_data_path', type=str, help="NoSQL persistence data path")

    # ObjectDatabase arguments
    parser.add_argument('--ObjectDatabase.name', type=str, help="Object database name")
    parser.add_argument('--ObjectDatabase.dir', type=str, help="Object database directory")
    parser.add_argument('--ObjectDatabase.max_faces', type=int, help="Object database max faces")

    # SQLDatabase arguments
    parser.add_argument('--SQLDatabase.name', type=str, help="SQL database name")
    parser.add_argument('--SQLDatabase.filename', type=str, help="SQL database filename")
    parser.add_argument('--SQLDatabase.persistence_data_path', type=str, help="SQL persistence data path")
    parser.add_argument('--SQLDatabase.sample_data', type=str, help="SQL sample data path")

    return parser.parse_args()

def preparation(config_path):
    cmd = ['python', 'function/preparation.py', '--config', config_path]
    subprocess.run(cmd)

def inference(config_path):
    cmd = ['python', 'function/inference.py', '--config', config_path]
    subprocess.run(cmd)

def main():
    args = parse_args()
    config = load_yaml(config_path=args.General.config)
    update_config(config, args)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_config_path = f'{args.General.temp_dir}/config_{timestamp}.yaml'
    save_config_to_yaml(config, temp_config_path)

    config_path = get_latest_config()
    assert config_path is not None, 'No configuration file found'

    mode = args.General.mode
    if mode == 'preparation':
        preparation(config_path=config_path)
    elif mode == 'inference':
        inference(config_path=config_path)

if __name__ == '__main__':
    main()