# Welcome to tame_your_files

|        |        |
|--------|--------|
| Package | [![Latest PyPI Version](https://img.shields.io/pypi/v/tame_your_files.svg)](https://pypi.org/project/tame_your_files/) [![Supported Python Versions](https://img.shields.io/pypi/pyversions/tame_your_files.svg)](https://pypi.org/project/tame_your_files/)  |
| Meta   | [![Code of Conduct](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md) |

*TODO: the above badges that indicate python version and package version will only work if your package is on PyPI.
If you don't plan to publish to PyPI, you can remove them.*

tame_your_files is an response to the perpetual forces of entropy that disorganize your digital workspace. Comprised of three main modules, this package is designed to tackle a specific aspect of file management, making it easier for users to maintain an organized and efficient digital environment:

* `file_size_utilities` helps users identify the largest files in their directories and determines the amount of space that can be freed up by deleting unnecessary files.
* `find_duplicates` scans directories to locate duplicate files, allowing users to reclaim storage space by removing redundant copies.
* `visualize_dir` provides graphical representations of user directories to improve file systems understanding and management.

Developers and data scientists alike will find tame_your_files to be a valuable tool as they accumulate projects and datasets over time. At the time of this writing, there are no other packages that combine these three functionalities into a single, cohesive tool.

## Get started

You can install this package into your preferred Python environment using pip:

```bash
$ pip install tame_your_files
```

TODO: Add a brief example of how to use the package to this section

To use tame_your_files in your code:

```python
>>> import tame_your_files
>>> tame_your_files.hello_world()
```

## Copyright

- Copyright © 2026 Ali Boolor, Jeffrey Ding, Eduardo Rivera.
- Free software distributed under the [MIT License](./LICENSE).
