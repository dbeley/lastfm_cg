# bot_lastfm_cg

Bot posting new lastfm_cg images found in a directory on twitter or mastodon.

The script needs a valid config file with twitter API keys (get them at [developer.twitter.com](https://developer.twitter.com).) and/or your mastodon account information in the same directory as the main script (see config_sample.ini for an example).

Use the systemd service in conjonction with lastfm_cg systemd services. Adjust the WorkingDirectory and ExecStart directive to match your configuration.

In order to run the script at a given time, some systemd services are provided in the systemd-service directory. You will have to change them to match your configuration, more specifically the WorkingDirectory and ExecStart directive.

## Requirements

- tweepy
- Mastodon.py

## Installation

Installation in a virtualenv with pipenv (recommended) :

```
pipenv install '-e .'
```

## Usage

Show the help and the available options.

```
bot_lastfm_cg.py -h
```

```
usage: bot_lastfm_cg [-h] [--debug] [-d DIRECTORY] [--no_upload]
                     [--social_media SOCIAL_MEDIA] [--timeframe TIMEFRAME]
                     [--template_file TEMPLATE_FILE]
                     [--config_file CONFIG_FILE]

Bot posting images from lastfm_cg to twitter or mastodon.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing the images to post (Default :
                        current directory).
  --no_upload           Disable the upload.
  --social_media SOCIAL_MEDIA, -s SOCIAL_MEDIA
                        Social media where the image will be posted (twitter,
                        mastodon or all. Default : all).
  --timeframe TIMEFRAME, -t TIMEFRAME
                        Only post pictures for a specific timeframe (Available
                        choices : 7day, 1month, 3month, 6month, 12month,
                        overall, all).
  --template_file TEMPLATE_FILE
                        Text file containing the template for the tweet
                        (Default : tweet_template.txt).
  --config_file CONFIG_FILE
                        Path to the config file (Default :
                        '~/Documents/lastfm_cg/bot_lastfm_cg/config.ini
```

## Systemd service

```
cp systemd-service/* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now twitter_bot_lastfm_cg_weekly.timer
``` 

## Template

The posted tweets will follow the template. See the tweet_template.txt file for an example.

Available variables :

- timeframe
- username
