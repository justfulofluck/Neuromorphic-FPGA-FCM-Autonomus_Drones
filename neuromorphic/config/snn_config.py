import yaml
from pathlib import Path

def load_config(path=None):
    if path is None:
        path = Path(__file__).parent / 'snn_config.yaml'
    with open(path) as f:
        config = yaml.safe_load(f)
    return config
