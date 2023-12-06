{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pythonEnv = pkgs.python311;
        poetryEnv = (pkgs.poetry.override { python3 = pythonEnv; });
        pkgs = import nixpkgs { 
          inherit system; 
          overlays = [
            (final: prev: rec {
              nodejs = prev.nodejs-18_x;
            })
          ];
            
        }; 
     in
      {
        devShells.default = pkgs.mkShell {
          #LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/";
          nativeBuildInputs = with pkgs; [
            pythonEnv
            poetryEnv
            pre-commit
            nodejs
          ];
        };
      });
}
