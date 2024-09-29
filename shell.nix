with import <nixpkgs> { };

let
  pythonPackages = python3Packages;
in pkgs.mkShell rec {
  name = "lastfmCgPythonEnv";
  venvDir = "~/Documents/venvs/lastfm_cg-venv";
  buildInputs = [
    pythonPackages.python

    pythonPackages.pytest
    pythonPackages.black
    pythonPackages.numpy
    pythonPackages.pandas
    pythonPackages.requests
    pythonPackages.pylast
    pythonPackages.tqdm
    pythonPackages.pillow
    pipenv
  ];

}
