import os
import yaml


def get_environment(suffix='CLOUD_SIMULATION_'):
    # load variables from environment if present
    config = {}
    for _key in os.environ.keys():
        if suffix not in _key:
            continue
        config.update({
            _key.split(suffix)[1].lower(): os.environ[_key]
            })
    return config


def get_config(config_path='/config/config.yaml', **kwargs):
    if os.path.exists(config_path):
        with open(config_path, 'r') as _f:
            config = yaml.load(_f, Loader=yaml.SafeLoader)
    else:
        config = {}
    return {**config, **kwargs}


def setup(**kwargs):
    # get and split config
    config = get_config(**get_environment())
    config.update(kwargs)
    return config
