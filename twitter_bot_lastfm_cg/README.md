# twitter_bot_lastfm_cg

Twitter bot posting new lastfm_cg images found in a directory.

Use the systemd services in conjonction with lastfm_cg systemd services.

lastfm_cg will create images every monday at 00:00, the Twitter bot will upload the new images found every monday at 09:00.

## Requirements

- tweepy

## Installation in a virtualenv (recommended)

```
pipenv install '-e .'
```

## Usage

```
twitter_bot_lastfm_cg.py
```

## Help

```
twitter_bot_lastfm_cg.py -h
```

```
usage: twitter_bot_lastfm_cg [-h] [--debug] [-d DIRECTORY]
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
