import os
import simplejson as json
from pkg_resources import resource_filename

from cloudbrain import core


def get_config():
    if os.environ.get("DEV"):
        config_file = resource_filename(core.__name__, 'config.dev.json')
    else:
        config_file = resource_filename(core.__name__, 'config.json')

    with open(os.path.join(config_file), 'rb') as f:
        json_config = json.load(f)

    auth_url = os.environ.get("AUTH_URL") or json_config['authUrl']
    rabbit_host = os.environ.get("RABBIT_HOST") or json_config['rabbitHost']

    config = {
        "authUrl": auth_url,
        "rabbitHost": rabbit_host
    }

    return config
