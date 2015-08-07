import os

def envcfg(config, env_prefix="ENV:", env_default_sep='='):
    """
    """

    # envcfg is a recursive function, so at the top-level it splits logic off
    # depending on input type

    if isinstance(config, dict):
        return {key: envcfg(val) for key, val in config.items()}

    if isinstance(config, list):
        return [envcfg(val) for val in config]

    if isinstance(config, tuple):
        return (envcfg(val) for val in config)

    elif isinstance(config, str):
        if config.startswith(env_prefix):
            # trim off the prefix
            env_key = config[len(env_prefix):]
            # split over the default separator
            env_key = env_key.split(env_default_sep, maxsplit=1)
            # if a default is set, store it
            if len(env_key) > 1:
                config_default = env_key[1]
            else:
                config_default = None
            # get the environment value from env_val
            env_val = os.environ.get(env_key[0], config_default)
            # check that a value was returned
            if env_val is None:
                raise KeyError("Environment variable not set: %s" % env_key[0])
            # parse numerically if possible
            try:
                return int(env_val)
            except ValueError:
                pass
            try:
                return float(env_val)
            except ValueError:
                pass
            return env_val
        else:
            return config

    elif isinstance(config, int) or isinstance(config, float):
        return config

    else:
        raise ValueError("Unsupported config type: %s" %
                type(config).__name__)


