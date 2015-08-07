import os

def envcfg(config, env_prefix="ENV:", env_default_sep='='):
    """Extract environment variables for a configuration object.

    This finds any string in the configuration object that starts with
    `env_prefix`, and replaces it with the corrseponding environment variable's
    value in the output.  If the key has a separator matching
    `env_default_sep`, any string after the separator is interpreted as the
    default value, to be used if that environment variable is not set.

    If an environment variable's value can be interpreted as an integer or a
    float, it will be cast to that type in the output.

    Args:
        config: the configuration object to parse.
            Can be of any type commonly found in serialized formats: dict,
            list, tuple, str, int, or float.

        env_prefix (str): The prefix to indicate an environment variable.

        env_default_sep (str): the separator to indicate a default value.

    Returns:
        A copy of the config object, with any relevant strings translated to
        environment variables.

    Raises:
        KeyError: If a value's environment variable is not set, and no default
            is provided.

        TypeError: If config is of an unsupported type.

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
        raise TypeError("Unsupported config type: %s" %
                type(config).__name__)


