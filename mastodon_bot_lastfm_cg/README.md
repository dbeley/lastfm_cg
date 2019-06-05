# mastodon_bot_lastfm_cg

Mastodon bot posting new lastfm_cg images found in a directory.

Use the systemd service in conjonction with lastfm_cg systemd services. Adjust the WorkingDirectory and ExecStart directive to match your configuration.

## Requirements

- valid config.ini file with mastodon api information in the script folder (see config_sample.ini for an example)

## Installation in a virtualenv (recommended)

```
pipenv install '-e .'
```

## Usage

```
mastodon_bot_lastfm_cg.py
```

## Help

```
mastodon_bot_lastfm_cg.py -h
```

```
usage: mastodon_bot_lastfm_cg [-h] [--debug] [-d DIRECTORY]
                              [--no_upload_mastodon]

Mastodon bot posting images from lastfm_cg

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  -d DIRECTORY, --directory DIRECTORY
                        Directory containing the images to post. Default :
                        current directory.
  --no_upload_mastodon  Disable the mastodon upload. Use it for debugging
```
