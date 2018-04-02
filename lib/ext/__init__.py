import yaml


def load_yaml_options(path):
    with open(path, 'r') as options_file:
        return yaml.load(options_file.read())
