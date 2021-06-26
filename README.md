# TurboTranscriber Language Server

## Dev Setup

### Install Server Dependencies

1. `python -m venv env`
2. Activate environment
3. `pip install pygls`
4. Create `.vscode/settings.json` file and set `python.pythonPath` to point to your python environment where `pygls` is installed

### Install Client Dependencies

Open terminal and execute following commands:

1. `npm install`
1. `cd client/ && npm install`

### Run Example

1. Open this directory in VS Code
1. Open debug view (`ctrl + shift + D`)
1. Select `Server + Client` and press `F5`


## TODO-List

- [x] get package.json right
- [x] publish to github
- [ ] Set up pipenv
- [ ] implement language (duh...)
- [ ] tests
