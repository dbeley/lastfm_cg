# bot_lastfm_cg

Bot posting new lastfm_cg images found in a directory on social media.

Use the systemd service in conjonction with lastfm_cg systemd services. Adjust the WorkingDirectory and ExecStart directive to match your configuration.

## Requirements

- tweepy
- valid config.ini file with api information in the script folder (see config_sample.ini for an example)

## Installation in a virtualenv (recommended)

```
pipenv install '-e .'
```

## Usage

```
bot_lastfm_cg.py
```

## Help

```
bot_lastfm_cg.py -h
```

```
usage: bot_lastfm_cg [-h] [--debug] [-d DIRECTORY]
                             [--no_upload_twitter]

Twitter bot posting images from lastfm_cg

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing the images to post. Default :
                        current directory.
  --no_upload_twitter   Disable the twitter upload. Use it for debugging
```
