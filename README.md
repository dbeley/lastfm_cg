# lastfm_cg : lastfm collage generator

[![Build Status](https://travis-ci.com/dbeley/lastfm_cg.svg?branch=master)](https://travis-ci.com/dbeley/lastfm_cg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0ee651b54bfd40d4aeece00298dd3fd0)](https://app.codacy.com/app/dbeley/lastfm_cg?utm_source=github.com&utm_medium=referral&utm_content=dbeley/lastfm_cg&utm_campaign=Badge_Grade_Dashboard)
[![codecov](https://codecov.io/gh/dbeley/lastfm_cg/branch/master/graph/badge.svg)](https://codecov.io/gh/dbeley/lastfm_cg)

<a href="docs/1month_2x3.png"><img src="docs/1month_2x3.png" width="390" height="260"/></a>

Generate covers collage from albums listened by a lastfm user.

This utility needs a valid config file with your lastfm API keys (get them at [last.fm/api](https://www.last.fm/api).) in ~/.config/lastfm_cg/config.ini (see config_sample.ini for an example).

It also caches the image files requested thanks to the requests-cache library. If you don't want the script to create an sqlite file in your ~/.local/share/lastfm_cg/ directory, you will have to launch the script with the -d/--disable_cache flag.

A twitter bot and a mastodon post are also available in the bot_lastfm_cg folder.

Some systemd service are also available int the systemd-service directory to run the lastfm_cg script at a given time. You will have to change them to match your configuration, more specifically the WorkingDirectory and ExecStart directive.

## Requirements

- pylast
- numpy
- pillow
- requests
- requests-cache
- tqdm

## Installation

Installation in a virtualenv with pipenv (recommended) :

```
git clone https://github.com/dbeley/lastfm_cg
cd lastfm_cg
pipenv install '-e .'
```

Classic installation :

```
pip install lastfm_cg
```

If you are an Archlinux user, you can install the AUR package [lastfm_cg-git](https://aur.archlinux.org/packages/lastfm_cg-git).

## Usage

Show the help and the available options.

```
lastfm_cg -h
```

```
usage: lastfm_cg [-h] [--debug] [--timeframe TIMEFRAME] [--rows ROWS]
                 [--columns COLUMNS] [--username USERNAME] [-d]

Create lastfm album collage for one or several lastfm users.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  --timeframe TIMEFRAME, -t TIMEFRAME
                        Timeframe (Accepted values : 7day, 1month, 3month,
                        6month, 12month, overall. Default : 7day).
  --rows ROWS, -r ROWS  Number of rows (Default : 5).
  --columns COLUMNS, -c COLUMNS
                        Number of columns (Default : number of rows).
  --username USERNAME, -u USERNAME
                        Usernames to extract, separated by comma.
  -d, --disable_cache   Disable the cache
```
 
Generate a collage for the user USER of the size 5x5 for the last 7 days (default values).

```
lastfm_cg -u USER
lastfm_cg -u USER -t 7day -r 5
```

Generate collages for the users USER and USER2 of the size 3x30 for all their listening history.

```
lastfm_cg -u USER,USER2 -t overall -r 3 -c 30
lastfm_cg --username USER,USER2 --timeframe overall --rows 3 --columns 30
```

## Sample results

<a href="docs/overall_5x8.png"><img src="docs/overall_5x8.png" width="800" height="500"/></a>

## Systemd service

```
cp systemd-service/* ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now lastfm_cg_weekly.timer
``` 
