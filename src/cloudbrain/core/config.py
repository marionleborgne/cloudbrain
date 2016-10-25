import json
import os


def get_config():
    core_path = os.path.join(os.getcwd(), 'src/cloudbrain/core')

    if os.environ.get("DEV", None):
        config_file = 'config.dev.json'
    else:
        config_file = 'config.json'

    with open(os.path.join(core_path, config_file), 'rb') as f:
        json_config = json.load(f)

    auth_url = os.environ.get("AUTH_URL", None) or json_config['authUrl']
    rabbit_host = os.environ.get("RABBIT_HOST", None) \
        or json_config['rabbitHost']

    config = {
        "authUrl": auth_url,
        "rabbitHost": rabbit_host
    }

    return config
