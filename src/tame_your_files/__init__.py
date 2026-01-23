# MIT License
#
# Copyright (c) 2026 Ali Boolor, Jeffrey Ding, Eduardo Rivera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Pure, non-destructive filesystem analysis utilities.
"""

from .file_size_utilities import FileInfo, files_to_free_space, largest_files
from .find_duplicates import (
    find_duplicates,
    find_duplicates_by_content,
    find_duplicates_by_name,
    find_duplicates_by_size,
)
from .visualize_dir import create_treemap_figure, get_directory_data, visualize_dir

__all__ = [
    "FileInfo",
    "largest_files",
    "files_to_free_space",
    "find_duplicates",
    "find_duplicates_by_name",
    "find_duplicates_by_size",
    "find_duplicates_by_content",
    "get_directory_data",
    "create_treemap_figure",
    "visualize_dir",
]
