import os

def envcfg(config, env_prefix="ENV:", env_default_sep='='):
    """
    """

    # envcfg is a recursive function, so at the top-level it splits logic off
    # depending on input type

    if isinstance(config, dict):
        return {key: envcfg(val) for key, val in config.items()}

    elif isinstance(config, str):
        if config.startswith(env_prefix):
            env_key = config[len(env_prefix):]
            env_key = config.split(env_default_sep, maxsplit=1)
            if len(config) > 1:
                config_default = env_key[1]
            else:
                config_default = None
            return os.environ.get(env_key[0], config_defaut)
        else:
            return config

    elif isinstance(config, int) or isinstance(config, float):
        return config

    else:
        raise ValueError("Unsupported config type: %s" %
                type(config).__name__)


