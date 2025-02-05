# timetable-ga

## Installation for MacOS

### Python

Either have Python 3.13 installed globally as default, or use pyenv to install Python 3.13 specifically to the project:

```
brew install pyenv
[ -f ~/.zshrc ] && echo 'eval "$(pyenv init -)"' >> ~/.zshrc
export PATH="$(pyenv root)/shims:$PATH" >> ~/.zshrc
exec "$SHELL"
pyenv install 3.13
pyenv local 3.13
```

### Dependencies

Manage Python dependencies with poetry.

```
# do this after `pyenv local 3.13`
# make sure this installs poetry version 1.8.4 or higher
pyenv exec pip3 install poetry
```

You have to add poetry to your PATH, by adding the following to your .zshrc:

```
export PATH="$HOME/.pyenv/shims/:$PATH"
```

Install dependencies:

```
cd ${PROJECT_HOME}  # where you've checked out the files
poetry install --no-root
```

### Development environment

In case of using VS Code, you have to set up the proper interpreter:

```
# check interpreter path of virtual env
poetry env info --path
```

Settings --> Python: Default Interpreter Path --> paste interpreter path /python3.13


## Start

To start project:

```
poetry run python -m uvicorn main:app --reload
```
