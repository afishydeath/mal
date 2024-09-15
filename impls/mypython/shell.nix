let
  pkgs = import (fetchTarball("channel:nixpkgs-unstable")) {};
in
  pkgs.mkShell {
    buildInputs = with pkgs; [
      python312
      pyright
      python312Packages.regex
      pylint
    ];
  }
