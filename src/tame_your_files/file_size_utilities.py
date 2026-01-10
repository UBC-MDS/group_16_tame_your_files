"""
File size utilities for analyzing disk usage.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileInfo:
    """
    Container for file metadata.

    Attributes
    ----------
    path : Path
        Absolute path to the file.
    size_bytes : int
        File size in bytes.
    """
    path: Path
    size_bytes: int


def largest_files(root: Path, n: int = 10) -> list[FileInfo]:
    """
    Recursively scan a directory and return the n largest files.

    Parameters
    ----------
    root : Path
        Root directory to scan. All subdirectories are included.
    n : int, default=10
        Maximum number of files to return.

    Returns
    -------
    list[FileInfo]
        Files sorted by size in descending order. At most n files
        are returned.

    Notes
    -----
    - Only regular files are considered.
    - Directories are ignored.
    - Unreadable files, broken symlinks, and permission errors
      are skipped silently.
    """
    pass


def files_to_free_space(root: Path, target_bytes: int) -> list[FileInfo]:
    """
    Determine the minimum number of files that would need to be deleted
    to free at least a given amount of disk space.

    This function DOES NOT delete anything.

    Parameters
    ----------
    root : Path
        Root directory to scan.
    target_bytes : int
        Desired amount of space to free, in bytes.

    Returns
    -------
    list[FileInfo]
        A list of files whose combined size is greater than or equal
        to target_bytes. Files are selected greedily, starting from
        the largest.

    Notes
    -----
    - Files are selected by descending size.
    - Selection stops as soon as the target is met.
    - If target_bytes <= 0, an empty list is returned.
    - If total file size is insufficient, all files are returned.
    - No files are deleted.
    """
    pass

