import configparser
import os
import pylast
import pytest


def load_config():
    user_config_dir = os.path.expanduser("~/.config/lastfm_cg/")
    secrets_file = user_config_dir + "config.ini"
    if os.path.isfile(secrets_file):
        config = configparser.ConfigParser()
        config.read(user_config_dir + "config.ini")
        api_key = config["lastfm"]["api_key"]
        api_secret = config["lastfm"]["api_secret"]
    else:
        try:
            api_key = os.environ["PYLAST_API_KEY"].strip()
            api_secret = os.environ["PYLAST_API_SECRET"].strip()
        except Exception as e:
            print(e)
            print("Problem while loading the config")
            exit()
    return api_key, api_secret


@pytest.fixture
def network_lastfm():
    api_key, api_secret = load_config()
    network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
    return network
