import pytest
import os
from tame_your_files.find_duplicates import (
    find_duplicates,
    find_duplicates_by_name,
    find_duplicates_by_size,
    find_duplicates_by_content
)

# LLM Transparency: These tests were manually written to cover the refined function specifications.
# I used Gemini AI to validate the test cases, ensuring that edge cases like 0-byte files,
# non-existent directories, and unique file sets were properly accounted for.

@pytest.fixture
def workspace(tmp_path):
    """
    Creates a temporary directory structure for testing.
    Structure:
    root/
      - file1.txt (content: "A", size: 1)
      - file2.txt (content: "B", size: 1)
      - sub1/
        - file1.txt (content: "A", size: 1) -> Duplicate name, content, size with root/file1.txt
        - file3.txt (content: "C", size: 1)
      - sub2/
        - file4.txt (content: "A", size: 1) -> Duplicate content, size with root/file1.txt
        - unique.txt (content: "Unique", size: 6)
    """
    d = tmp_path / "workspace"
    d.mkdir()
    
    sub1 = d / "sub1"
    sub1.mkdir()
    
    sub2 = d / "sub2"
    sub2.mkdir()
    
    # Create files
    (d / "file1.txt").write_text("A", encoding="utf-8")
    (d / "file2.txt").write_text("B", encoding="utf-8")
    
    (sub1 / "file1.txt").write_text("A", encoding="utf-8")
    (sub1 / "file3.txt").write_text("C", encoding="utf-8")
    
    (sub2 / "file4.txt").write_text("A", encoding="utf-8")
    (sub2 / "unique.txt").write_text("Unique", encoding="utf-8")
    
    return d

def test_find_duplicates_by_name(workspace):
    """Test finding duplicates by file name."""
    result = find_duplicates_by_name(str(workspace))
    
    assert isinstance(result, dict)
    
    # 'file1.txt' appears twice
    assert "file1.txt" in result
    assert len(result["file1.txt"]) == 2
    
    # Check paths (order might vary, so use set or verify existence)
    paths = [os.path.normpath(p) for p in result["file1.txt"]]
    expected_1 = os.path.normpath(str(workspace / "file1.txt"))
    expected_2 = os.path.normpath(str(workspace / "sub1" / "file1.txt"))
    
    assert expected_1 in paths
    assert expected_2 in paths

    # 'file2.txt' appears once, so it should NOT be in the duplicates dict?
    # The docstring says "keys are file names and values are lists of file paths that have that name (i.e., are duplicates)."
    # Usually, if there's only one, it's not a duplicate. However, the docstring is slightly ambiguous.
    # "values are lists of file paths that have that name". 
    # If a file is unique, it has a name, but is it a "duplicate"?
    # The function name is "find_duplicates", implying only duplicates should be returned.
    # We will assume only actual duplicates (count > 1) are returned.
    assert "file2.txt" not in result
    assert "unique.txt" not in result

def test_find_duplicates_by_size(workspace):
    """Test finding duplicates by file size."""
    # file1.txt (1 byte), file2.txt (1 byte), sub1/file1.txt (1 byte), sub1/file3.txt (1 byte), sub2/file4.txt (1 byte)
    # unique.txt (6 bytes)
    
    result = find_duplicates_by_size(str(workspace))
    
    assert isinstance(result, dict)
    
    # Size 1 has 5 files
    assert 1 in result
    assert len(result[1]) == 5
    
    # Size 6 has 1 file, should not be in result
    assert 6 not in result

def test_find_duplicates_by_content(workspace):
    """Test finding duplicates by content (hash)."""
    # Content "A": root/file1.txt, sub1/file1.txt, sub2/file4.txt (3 copies)
    # Content "B": root/file2.txt (1 copy)
    # Content "C": sub1/file3.txt (1 copy)
    # Content "Unique": sub2/unique.txt (1 copy)
    
    result = find_duplicates_by_content(str(workspace))
    
    assert isinstance(result, dict)
    
    # We don't know the exact hash algorithm yet, but we can check if there is a key with 3 values
    # and verify those values are the correct files.
    
    found_duplicates = False
    for k, v in result.items():
        if len(v) == 3:
            found_duplicates = True
            paths = [os.path.normpath(p) for p in v]
            assert os.path.normpath(str(workspace / "file1.txt")) in paths
            assert os.path.normpath(str(workspace / "sub1" / "file1.txt")) in paths
            assert os.path.normpath(str(workspace / "sub2" / "file4.txt")) in paths
            
    assert found_duplicates, "Should have found one group of 3 duplicate files (content 'A')"
    
    # Check that unique contents are not included
    # Count of keys with length 1 should be 0
    for k, v in result.items():
        assert len(v) > 1

def test_find_duplicates_main_function(workspace):
    """Test the main wrapper function."""
    
    # Test default method (content)
    result_content = find_duplicates(str(workspace))
    # Should be same as by_content
    found_A = False
    for k, v in result_content.items():
        if len(v) == 3:
            found_A = True
    assert found_A
    
    # Test method='name'
    result_name = find_duplicates(str(workspace), method='name')
    assert "file1.txt" in result_name
    assert len(result_name["file1.txt"]) == 2
    
    # Test method='size'
    result_size = find_duplicates(str(workspace), method='size')
    assert 1 in result_size
    assert len(result_size[1]) == 5

def test_find_duplicates_invalid_method(workspace):
    """Test that an invalid method raises an error or handles gracefully."""
    # Depending on implementation, might raise ValueError.
    # Assuming it should raise ValueError for now.
    with pytest.raises(ValueError):
        find_duplicates(str(workspace), method='invalid_method')

def test_find_duplicates_invalid_directory():
    """Test that a FileNotFoundError is raised for an invalid directory."""
    with pytest.raises(FileNotFoundError):
        find_duplicates("non_existent_directory_12345")

    with pytest.raises(FileNotFoundError):
        # Pass a file path instead of a directory
        find_duplicates(__file__) 

def test_find_duplicates_zero_byte_files(tmp_path):
    """Test handling of 0-byte files."""
    d = tmp_path / "zero_byte"
    d.mkdir()
    (d / "empty1").touch()
    (d / "empty2").touch()
    (d / "not_empty").write_text("content")

    # By size: 0 bytes
    res_size = find_duplicates(str(d), method='size')
    assert 0 in res_size
    assert len(res_size[0]) == 2
    
    # By content: empty hash (d41d8cd98f00b204e9800998ecf8427e is MD5 of empty string)
    res_content = find_duplicates(str(d), method='content')
    empty_hash = "d41d8cd98f00b204e9800998ecf8427e"
    assert empty_hash in res_content
    assert len(res_content[empty_hash]) == 2

def test_find_duplicates_no_duplicates(tmp_path):
    """Test directory with files but no duplicates."""
    d = tmp_path / "unique"
    d.mkdir()
    # Initialize with different content and sizes immediately
    (d / "f1").write_text("a")
    (d / "f2").write_text("bb")
    (d / "f3").write_text("ccc")

    assert find_duplicates(str(d), method='name') == {}
    assert find_duplicates(str(d), method='size') == {}
    assert find_duplicates(str(d), method='content') == {}

def test_empty_directory(tmp_path):
    """Test behavior with an empty directory."""
    d = tmp_path / "empty"
    d.mkdir()
    
    # Direct function calls
    assert find_duplicates_by_name(str(d)) == {}
    assert find_duplicates_by_size(str(d)) == {}
    assert find_duplicates_by_content(str(d)) == {}
    
    # Wrapper calls
    assert find_duplicates(str(d), method='name') == {}
    assert find_duplicates(str(d), method='size') == {}
    assert find_duplicates(str(d), method='content') == {}
