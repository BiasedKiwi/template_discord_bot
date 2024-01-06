from pathlib import Path

import yaml


def clean_values(input_dict, output_dict=None):
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
        print(_dict)

    clean = clean_values(_dict)
    return clean
