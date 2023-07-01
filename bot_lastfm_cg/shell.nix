with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "lastfmCgPythonEnv";
  venvDir = "~/Documents/venvs/lastfm_cg-venv";
  buildInputs = [
    pythonPackages.python

    pythonPackages.numpy
    pythonPackages.pandas
    pythonPackages.requests
    pythonPackages.requests-cache
    pythonPackages.pylast
    pythonPackages.tqdm
    pythonPackages.pillow
    pythonPackages.tweepy
    pythonPackages.mastodon-py
    pipenv
  ];

}
