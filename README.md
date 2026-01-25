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

Build the Quarto site (this runs `quartodoc` automatically via `pre-render`):

```bash
quarto render docs
```

## Deploying documentation (automated)

![Build Status](https://github.com/UBC-MDS/group_16_tame_your_files.git/actions/workflows/publish-test-pypi.yml/badge.svg)
Documentation is built and deployed automatically to GitHub Pages via GitHub Actions.
Live site: https://github.com/UBC-MDS/group_16_tame_your_files
