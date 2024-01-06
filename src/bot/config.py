from pathlib import Path

import yaml


def clean_values(_dict):
    values = {}
    for item in _dict.items():
        try:
            for key, value in item[1][0].items():
                values[key] = value
        except KeyError:
            for key, value in item[1].items():
                values[key] = value
    return values

def get_raw_config(path: str = Path(__file__).parent / "config.yaml"):
    """Being deprecated. Return a raw dict of the config file (using `yaml.load`)"""
    with open(path, encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)
        return _dict

def load_config(path: str = Path(__file__).parent / "config.yaml"):
    with open(path, encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)

    clean = clean_values(_dict)
    return clean

def load_theme(path: str = Path(__file__).parent / "theme.yaml"):
    with open(path, encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)
        
    clean = clean_values(_dict)
    return clean
