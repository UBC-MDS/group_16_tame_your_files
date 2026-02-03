# tame_your_files

[![TestPyPI](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Ftest.pypi.org%2Fpypi%2Fgroup-16-tame-your-files%2Fjson&query=info.version&label=TestPyPI)](https://test.pypi.org/project/group-16-tame-your-files/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Build and Test](https://github.com/UBC-MDS/group_16_tame_your_files/actions/workflows/build.yml/badge.svg)](https://github.com/UBC-MDS/group_16_tame_your_files/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/UBC-MDS/group_16_tame_your_files/branch/dev/graph/badge.svg)](https://codecov.io/gh/UBC-MDS/group_16_tame_your_files)

## Project overview

`tame_your_files` provides pure, non-destructive filesystem analysis utilities.
It can identify large files, suggest candidates to free space, find duplicates, and
visualize directory structures.

Documentation: [https://ubc-mds.github.io/group_16_tame_your_files/](https://ubc-mds.github.io/group_16_tame_your_files/)

## User-facing functions

- File size utilities: `FileInfo`, `largest_files`, `files_to_free_space`
- Duplicate detection: `find_duplicates`, `find_duplicates_by_name`, `find_duplicates_by_size`, `find_duplicates_by_content`
- Directory visualization: `get_directory_data`, `create_treemap_figure`, `visualize_dir`

## Comparisons

`tame_your_files` is a lightweight Python API for analysis only (no deletion).
Compared with common CLI and GUI tools, it is designed for reproducible, scriptable workflows:

- CLI duplicate finders (e.g., `fdupes`) focus on terminal workflows; `tame_your_files` exposes Python functions you can compose in notebooks and scripts.
- Disk usage tools (e.g., `ncdu`) are interactive; `tame_your_files` returns structured data you can visualize or export.
- GUI apps (e.g., dupeGuru) provide point-and-click workflows; `tame_your_files` targets programmatic use in data pipelines.

## Motivation

Standard tools like `mv` and `find` are powerful, but they are low-level and imperative.
`tame_your_files` is useful when you want to *analyze first* and take action later:

- Non-destructive by design: functions return data instead of modifying files.
- Reproducible workflows: run the same analysis in scripts or notebooks and share results.
- Structured outputs: get Python objects you can filter, visualize, or export.
- Safer cleanup: identify candidates before you delete or move anything.

## Examples

### File size utilities

```python
from pathlib import Path
import tempfile
from tame_your_files.file_size_utilities import FileInfo, largest_files, files_to_free_space

info = FileInfo(path=Path("example.txt"), size_bytes=12)
print(info.path.name, info.size_bytes)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "a.txt").write_text("a")
    (root / "b.txt").write_text("bbb")

    biggest = largest_files(root, n=1)
    print([f.path.name for f in biggest])

    to_delete = files_to_free_space(root, target_bytes=2)
    print([f.path.name for f in to_delete])
```

### Duplicate detection

```python
import tempfile
from pathlib import Path
from tame_your_files.find_duplicates import (
    find_duplicates,
    find_duplicates_by_name,
    find_duplicates_by_size,
    find_duplicates_by_content,
)

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "a.txt").write_text("same")
    (root / "b.txt").write_text("same")
    (root / "c.txt").write_text("diff")

    print(find_duplicates(root, method="content"))
    print(find_duplicates_by_name(root))
    print(find_duplicates_by_size(root))
    print(find_duplicates_by_content(root))
```

### Directory visualization

```python
from tame_your_files.visualize_dir import (
    get_directory_data,
    create_treemap_figure,
    visualize_dir,
)

data = get_directory_data(".")
fig = create_treemap_figure(data)
# fig.show()

fig2 = visualize_dir(".")
# fig2.show()
```

## Development environment setup

Create and activate the conda environment defined in `environment.yml`:

```bash
conda env create -f environment.yml
conda activate tame_your_files_env
```

## Installation

Choose one of the following:

### Install from PyPI (recommended for most users)

```bash
python -m pip install tame_your_files
```

### Install from TestPyPI (pre-release testing)

```bash
python -m pip install -i https://test.pypi.org/simple/ tame_your_files
```

### Install from source (for development)

Clone the repository, then install in editable mode from the repo root:

```bash
git clone https://github.com/UBC-MDS/group_16_tame_your_files.git
cd group_16_tame_your_files
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
