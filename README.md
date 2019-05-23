# lastfm_cg : lastfm collage generator

Generate covers collage from album listened by a lastfm user.

Needs a valid config file with your API lastfm keys (get them at https://www.last.fm/api) in ~/.config/lastfm_cg/ directory.

## Installation

```
pip install lastfm_cg
```

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

Generate a collage for the user USER of the size 3x3 for all its history.

```
lastfm_cg -u USER -t overall -r 3
lastfm_cg --username USER --timeframe overall --rows 3
```
