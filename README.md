# lastfm_cg : lastfm collage generator

<a href="docs/1month_2x3.png"><img src="docs/1month_2x3.png" width="390" height="260"/></a>

Generate covers collage from albums listened by a lastfm user.

This utility needs a valid config file with your lastfm API keys (get them at https://www.last.fm/api) in ~/.config/lastfm_cg/config.ini (see config_sample.ini for an example).

It also cache the image file requested thanks to the requests-cache library. If you don't want the script to create an sqlite file in your ~/.local/share/lastfm_cg/ folder, you will have to launch the script with the -d/--disable_cache flag.

A twitter bot and a mastodon post are also supplied.


## Requirements

- pylast
- numpy
- pillow
- requests
- requests-cache
- tqdm

## Installation

```
pip install lastfm_cg
```

If you are an Archlinux user, you can install the AUR package [lastfm_cg-git](https://aur.archlinux.org/packages/lastfm_cg-git).

## Installation in a virtualenv

```
git clone https://github.com/dbeley/lastfm_cg
cd lastfm_cg
pipenv install '-e .'
```

## Usage

Show the help and the available options.

```
lastfm_cg -h
```

```
usage: lastfm_cg [-h] [--debug] [--timeframe TIMEFRAME] [--rows ROWS]
                 [--columns COLUMNS] [--username USERNAME] [-d]

Create lastfm album collage for an user

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information
  --timeframe TIMEFRAME, -t TIMEFRAME
                        Timeframe (Accepted values : 7day, 1month, 3month,
                        6month, 12month, overall. Default : 7day).
  --rows ROWS, -r ROWS  Number of rows (Maximum value : 31. Default : 5).
  --columns COLUMNS, -c COLUMNS
                        Number of columns (Maximum value : 31. Default :
                        number of rows).
  --username USERNAME, -u USERNAME
                        Usernames to extract (separated by comma)
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

## Samples Results

<a href="docs/overall_5x8.png"><img src="docs/overall_5x8.png" width="800" height="500"/></a>
