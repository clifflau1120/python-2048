# The 2048 Game

A CLI implementation of the 2048 game, written in Python.

## Getting started

### Installation

If you have [`pipx`](https://github.com/pypa/pipx) installed:

```zsh
pipx install git@github.com:clifflau1120/python-2048.git
```

or you can build from source with [uv](https://github.com/astral-sh/uv):

```zsh
git clone git@github.com:clifflau1120/python-2048.git
cd python-2048

uv python install 3.13      # install Python 3.13
uv python pin 3.13          # pin Python 3.13
uv venv                     # create a virtual environment
source .venv/bin/activate   # activate the virtual environment
uv sync                     # sync dependencies to the virtual environment
```

### Run the game

To start a new game:

```zsh
python-2048 run
```

To continue from a previously saved snapshot:

```zsh
python-2048 run <game_snapshot_path>
```

To enable LLM-based suggestion, as supported by [`pydantic_ai`](https://ai.pydantic.dev/models/#models-and-providers):

```zsh
python-2048 run --model <model_name>
```

To observe how an LLM plays 2048:

```zsh
python-2048 run --impersonate --model <model_name>
```

# Contributing

This repository uses `ruff` for formatting and linting:

```zsh
ruff format
ruff check
```

... and `pyright` for type checking:

```zsh
pyright
```

... as well as `pytest` for testing:

```zsh
pytest
```

You can install [pre-commit](https://pre-commit.com/) hooks so that code quality is verified on each commit:

```zsh
pre-commit install
```

## Versioning

This repository uses calendar versioning.
