# tame_your_files

[![Build and Test](https://github.com/UBC-MDS/group_16_tame_your_files/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/group_16_tame_your_files/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/UBC-MDS/group_16_tame_your_files/branch/main/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/group_16_tame_your_files)

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

Documentation is built by GitHub Actions and published to the `gh-pages` branch.
To enable GitHub Pages:

1. Go to `Settings` → `Pages`.
2. Set **Source** to **Deploy from a branch**.
3. Select branch `gh-pages` and folder `/(root)`, then save.
4. After the first workflow run, the Pages URL will appear on the same screen.

To force a rebuild, run the `quarto-publish` workflow from the **Actions** tab
using **Run workflow**.
