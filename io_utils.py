import yaml


def read_yaml(filepath):
    with open(filepath, "r") as f:
        yml = yaml.safe_load(f)
    return yml
