'''
This will be a set of functions to find duplicate files in a given directory and subdirectories. There will be several "modes" of finding duplicates, such as by file name, by file size, and by file content (hashing).
In order for the functions to be testable, we would like them to return something that can be easily asserted. For example, a dictionary where keys are the duplicate identifiers (like file name, size, or hash) and values are lists of file paths that match that identifier.

'''

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
        A dictionary where keys are file hashes and values are lists of file paths
        that have that hash (i.e., are duplicates).
    """
    # Implementation will go here
    pass

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
        that have that name (i.e., are duplicates).
    """
    # Implementation will go here
    pass

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
        A dictionary where keys are file sizes and values are lists of file paths
        that have that size (i.e., are duplicates).
    """
    # Implementation will go here
    pass

def find_duplicates_by_content(directory):
    """
    Finds duplicate files based on file content (hashing) within a given directory and its subdirectories.

    Parameters
    ----------
    directory : str
        The path to the directory to search for duplicates.
    
    Returns
    -------
    dict
        A dictionary where keys are file hashes and values are lists of file paths
        that have that hash (i.e., are duplicates).
    """
    # Implementation will go here
    pass
