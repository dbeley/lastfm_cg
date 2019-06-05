# mastodon_bot_lastfm_cg

Mastodon bot posting new lastfm_cg images found in a directory.

Use the systemd service in conjonction with lastfm_cg systemd services. Adjust the WorkingDirectory and ExecStart directive to match your configuration.

lastfm_cg will create images every monday at 00:00, the Twitter bot will upload the new images found every monday at 09:00.

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
```
