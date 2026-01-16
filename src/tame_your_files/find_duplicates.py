'''
This will be a set of functions to find duplicate files in a given directory and subdirectories. There will be several "modes" of finding duplicates, such as by file name, by file size, and by file content (hashing).
In order for the functions to be testable, we would like them to return something that can be easily asserted. For example, a dictionary where keys are the duplicate identifiers (like file name, size, or hash) and values are lists of file paths that match that identifier.
Author: Eduardo Rivera
'''
import os
import hashlib
from collections import defaultdict

def find_duplicates(directory, method='content'):
    """
    Finds duplicate files within a given directory and its subdirectories. This is the main function that will call the other functions.

    Parameters
    ----------
    directory : str
        The path to the directory to search for duplicates.
    method : str, optional
        The method to use for finding duplicates. Can be 'name', 'size', or 'content'.
        Defaults to 'content'.

    Returns
    -------
    dict
        A dictionary where keys are the duplicate identifiers (hash, name, or size) 
        and values are lists of file paths that match that identifier.
        Returns an empty dictionary if no duplicates are found.

    Raises
    ------
    ValueError
        If the provided method is not one of 'name', 'size', or 'content'.
    FileNotFoundError
        If the provided directory path does not exist or is not a directory.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist or is not a directory.")

    if method == 'name':
        return find_duplicates_by_name(directory)
    elif method == 'size':
        return find_duplicates_by_size(directory)
    elif method == 'content':
        return find_duplicates_by_content(directory)
    else:
        raise ValueError(f"Invalid method: {method}. Must be 'name', 'size', or 'content'.")

def find_duplicates_by_name(directory):
    """
    Finds duplicate files based on file names within a given directory and its subdirectories.

    Parameters
    ----------
    directory : str
        The path to the directory to search for duplicates.

    Returns
    -------
    dict
        A dictionary where keys are file names and values are lists of file paths
        that have that name. Only includes names that appear more than once.
    """
    files_by_name = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            files_by_name[file].append(os.path.join(root, file))
            
    return {name: paths for name, paths in files_by_name.items() if len(paths) > 1}

def find_duplicates_by_size(directory):
    """
    Finds duplicate files based on file sizes within a given directory and its subdirectories.

    Parameters
    ----------
    directory : str
        The path to the directory to search for duplicates.

    Returns
    -------
    dict
        A dictionary where keys are file sizes (in bytes) and values are lists of file paths
        that have that size. Only includes sizes that appear more than once.
    """
    files_by_size = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                # We do not skip 0-byte files; two empty files are considered duplicates by size.
                size = os.path.getsize(path)
                files_by_size[size].append(path)
            except OSError:
                # Handle cases where file might be deleted or permissions issue
                continue
            
    return {size: paths for size, paths in files_by_size.items() if len(paths) > 1}

def find_duplicates_by_content(directory):
    """
    Finds duplicate files based on file content (MD5 hash) within a given directory and its subdirectories.

    Parameters
    ----------
    directory : str
        The path to the directory to search for duplicates.

    Returns
    -------
    dict
        A dictionary where keys are file hashes and values are lists of file paths
        that have that hash. Only includes hashes that appear more than once.
    """
    files_by_hash = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                hash_md5 = hashlib.md5()
                with open(path, "rb") as f:
                    # Read in chunks to handle large files memory-efficiently
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                files_by_hash[hash_md5.hexdigest()].append(path)
            except OSError:
                continue
            
    return {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}
