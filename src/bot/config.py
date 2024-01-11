from pathlib import Path
from typing import Dict

import yaml


def clean_values(input_dict, output_dict=None) -> Dict[str, str]:
    if output_dict is None:
        output_dict = {}

    for key, value in input_dict.items():
        new_key = key

        if isinstance(value, dict):
            clean_values(value, output_dict)
        elif isinstance(value, list):
            for idx, item in enumerate(value):
                if isinstance(item, dict):
                    clean_values(item, output_dict)
                else:
                    output_dict[f"{new_key}[{idx}]"] = item
        else:
            output_dict[new_key] = value

    return output_dict


def load_config() -> Dict[str, str]:
    """Generate a dict based on the theme configuration file"""
    with open(Path(__file__).parent / "config.yaml", encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)

    clean = clean_values(_dict)
    return clean


def load_theme() -> Dict[str, str]:
    """Generate a dict based on the theme configuration file"""
    with open(Path(__file__).parent / "theme.yaml", encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)

    clean = clean_values(_dict)
    return clean
