import yaml


def load_yaml(args, path="."):
    """load yaml file
    Args:
        args (argparse): Python argparse that contains arguments
        path (str): Root directory to load config from. Default: "."
    """
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    for key, value in config.items():
        args.__dict__[key] = value
