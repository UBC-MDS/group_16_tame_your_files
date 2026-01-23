# tame_your_files

## Project overview

`tame_your_files` provides pure, non-destructive filesystem analysis utilities.
It can identify large files, suggest candidates to free space, find duplicates, and
visualize directory structures.

## Development environment setup

Create and activate the conda environment defined in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate tame_your_files_env
```

## Installation

Install the package in editable (development) mode from the repository root:

```bash
python -m pip install -e .
```

## Running tests

Run the full test suite from the repository root:

```bash
python -m pytest
```

## Building documentation locally

Install the Quarto extension and Python dependency, then build the site:

```bash
cd docs
quarto add quarto-ext/quartodoc
python -m pip install quartodoc
QUARTO_PYTHON="$(which python)" quarto render
```

## Deploying documentation (automated)

Documentation is built and deployed automatically to GitHub Pages via GitHub Actions.
Live site: <https://<GITHUB_PAGES_URL>>
