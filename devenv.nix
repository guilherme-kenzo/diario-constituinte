{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [ 
    pkgs.git
    pkgs.tesseract4
    pkgs.poppler_utils
    pkgs.mupdf
    pkgs.bashInteractive
    pkgs.nix-bash-completions
    pkgs.bash-completion
  ];

  # https://devenv.sh/scripts/
  scripts.hello.exec = "echo hello from $GREET";

  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep "2.42.0"
  '';


  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      install = {
        enable = true;
        installRootPackage = false;
        onlyInstallRootPackage = false;
        compile = false;
        quiet = false;
        groups = [ ];
        ignoredGroups = [ ];
        onlyGroups = [ ];
        extras = [ ];
        allExtras = false;
        verbosity = "no";
      };
      activate.enable = true;
      package = pkgs.poetry;
    };
  };
  
  env = {
    LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  };

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/languages/
  # languages.nix.enable = true;

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
