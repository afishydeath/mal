let
  pkgs = import (fetchTarball("channel:nixpkgs-unstable")) {};
in
  pkgs.mkShell {
    buildInputs = with pkgs; [
      python3
      pyright
      python3Packages.regex
    ];
  }
