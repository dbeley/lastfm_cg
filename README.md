# lastfm_cg : lastfm collage generator

Generate covers collage from albums listened by a lastfm user.

This utility needs a valid config file with your lastfm API keys (get them at https://www.last.fm/api) in ~/.config/lastfm_cg/config.ini (see config_sample.ini for an example).

It also cache the image file requested thanks to the requests-cache library. If you don't want the script to create an sqlite file in your ~/.local/share/lastfm_cg/ folder, you will have to launch the script with the -d/--disable_cache flag.

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

Generate a collage for the user USER of the size 5x5 for the last 7 days (default values).

```
lastfm_cg -u USER
lastfm_cg -u USER -t 7day -r 5
```

Generate a collage for the user USER of the size 3x30 for all its history.

```
lastfm_cg -u USER -t overall -r 3 -c 30
lastfm_cg --username USER --timeframe overall --rows 3 --columns 30
```
