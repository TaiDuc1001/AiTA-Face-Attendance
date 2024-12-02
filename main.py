from utils import save_config_to_yaml, get_latest_config, convert_to_dict
import subprocess
from datetime import datetime
import argparse
import nestargs

def parse_args():
    parser = nestargs.NestedArgumentParser(
        description='AiTA Attendance Checking System with Weaviate and InsightFace',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # General arguments
    parser.add_argument('--General.mode', type=str, required=True, help="Mode of operation (preparation/inference)")
    parser.add_argument('--General.config', type=str, default='config.yaml', help="Path to configuration file")
    parser.add_argument('--General.load_samples', action='store_true', help="Load default samples")
    parser.add_argument('--General.temp_dir', type=str, default='configs', help="Temporary configs directory")

    # Camera configuration
    parser.add_argument('--Camera.name', type=str, help="Camera name")
    parser.add_argument('--Camera.url', type=str, help="Input URL")

    # Detector configuration
    parser.add_argument('--Detector.name', type=str, help="Detector name")
    parser.add_argument('--Detector.path', type=str, help="Path for detector")

    # Recognizer configuration
    parser.add_argument('--Recognizer.name', type=str, help="Recognizer name")

    # NoSQL Database configuration
    parser.add_argument('--NoSQLDatabase.name', type=str, help="NoSQL database name")
    parser.add_argument('--NoSQLDatabase.hostname', type=str, help="NoSQL hostname")
    parser.add_argument('--NoSQLDatabase.port', type=int, help="NoSQL port")
    parser.add_argument('--NoSQLDatabase.persistence_path', type=str, help="NoSQL persistence data path")

    # Object Database configuration
    parser.add_argument('--ObjectDatabase.name', type=str, help="Object database name")
    parser.add_argument('--ObjectDatabase.dir', type=str, help="Object database directory")
    parser.add_argument('--ObjectDatabase.max_faces', type=int, help="Object database max faces")

    # SQL Database configuration
    parser.add_argument('--SQLDatabase.name', type=str, help="SQL database name")
    parser.add_argument('--SQLDatabase.filename', type=str, help="SQL database filename")
    parser.add_argument('--SQLDatabase.persistence_path', type=str, help="SQL persistence data path")
    parser.add_argument('--SQLDatabase.sample_data', type=str, help="SQL sample data path")

    return parser.parse_args()

def preparation(config_path):
    """Run the preparation script with the given config path."""
    cmd = ['python', 'function/preparation.py', '--config', config_path]
    subprocess.run(cmd, check=True)

def inference(config_path):
    """Run the inference script with the given config path."""
    cmd = ['python', 'function/inference.py', '--config', config_path]
    subprocess.run(cmd, check=True)

def main():
    args = parse_args()
    config = convert_to_dict(args)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_config_path = f"{config['General']['temp_dir']}/{timestamp}_config.yaml"
    save_config_to_yaml(config, temp_config_path)

    config_path = get_latest_config()
    if config_path is None:
        raise FileNotFoundError('No configuration file found')

    if config['General']['mode'] == 'preparation':
        preparation(config_path=config_path)
    elif config['General']['mode'] == 'inference':
        inference(config_path=config_path)
    else:
        raise ValueError(f"Invalid mode: {config['General']['mode']}. Must be 'preparation' or 'inference'")

if __name__ == '__main__':
    main()