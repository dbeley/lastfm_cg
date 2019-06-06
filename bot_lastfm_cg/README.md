# bot_lastfm_cg

Bot posting new lastfm_cg images found in a directory on twitter or mastodon.

Use the systemd service in conjonction with lastfm_cg systemd services. Adjust the WorkingDirectory and ExecStart directive to match your configuration.

## Requirements

- tweepy
- Mastodon.py
- valid config.ini file with api/account information in the script folder (see config_sample.ini for an example)

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
usage: bot_lastfm_cg [-h] [--debug] [-d DIRECTORY] [--no_upload]
                     [--social_media SOCIAL_MEDIA]

Bot posting images from lastfm_cg to twitter or mastodon.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing the images to post. Default :
                        current directory.
  --no_upload           Disable the upload. Use it for debugging
  --social_media SOCIAL_MEDIA, -s SOCIAL_MEDIA
                        Social media where the image will be posted (twitter
                        or mastodon. Default = twitter).
```
