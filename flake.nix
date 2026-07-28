{
  description = "lastfm_cg - Last.fm collage generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        pythonPackages = python.pkgs;
        pythonEnv = python.withPackages (ps: with ps; [
          pylast numpy pillow requests tqdm
        ]);
      in
      {
        packages.default = pythonPackages.buildPythonPackage {
          pname = "lastfm_cg";
          version = "1.6.0";
          pyproject = true;
          src = ./.;
          nativeBuildInputs = [ pythonPackages.hatchling ];
          propagatedBuildInputs = with pythonPackages; [ pylast numpy pillow requests tqdm ];
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv pythonPackages.ruff pythonPackages.pytest pythonPackages.pytest-cov ];
        };
      });
}
