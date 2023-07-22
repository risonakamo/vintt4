# vintt4
time tracker v4

track time of programs with sub categories per program

# requirements
- python conda environment (3.9+)
- relatively up to date node (for building web assets)

# installation
1. `git submodule update --init --recursive`
2. in the vintt3-web folder:
    - `npm i`
    - `npm run build`
1. `git submodule update --init --recursive`
2. in the vintt3-web folder:
    - `npm i`
    - `npm run build`
1. in your selected conda env, `pip install -e .` this repo
2. modify `bin/run-vintt4-installed.bat` to have the name of your conda env
3. create `bin/vinttconfig.yml` with your options

# run options
- double click: to run from file explorer, double click `run-vintt4-installed.bat`. a shortcut can be made to this file for running from a different location
- dev mode: for running from command line, `run-vintt4.bat`. use `stop-vintt4.bat` to end