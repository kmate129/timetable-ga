# timetable-ga

## Installation for MacOS

### Python

Either have Python 3.12 installed globally as default, or use pyenv to install Python 3.12 specifically to the project:

```
brew install pyenv
[ -f ~/.zshrc ] && echo 'eval "$(pyenv init -)"' >> ~/.zshrc
export PATH="$(pyenv root)/shims:$PATH" >> ~/.zshrc
exec "$SHELL"
pyenv install 3.12
pyenv local 3.12
```

### Dependencies

Manage Python dependencies with poetry.

```
# do this after `pyenv local 3.12`
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
poetry install
```