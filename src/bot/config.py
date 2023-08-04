import yaml


def get_raw_config(path: str = "./bot/config.yaml"):
    """Return a raw dict of the config file (using `yaml.load`)"""
    with open(path, encoding="utf-8") as file:
        _dict = yaml.load(file, Loader=yaml.FullLoader)
        return _dict
