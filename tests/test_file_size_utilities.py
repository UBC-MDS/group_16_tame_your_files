"""
Tests for file_size_utilities module.
"""
import pytest
from pathlib import Path
from tame_your_files.file_size_utilities import FileInfo, largest_files, files_to_free_space


def test_largest_files_basic(tmp_path):
    """
    Test largest_files basic functionality.
    
    Create multiple files with known sizes and verify:
    - Correct number of results
    - Correct descending order
    - Correct file sizes
    """
    # Create files with different sizes
    files_data = [
        ("small.txt", 100),
        ("medium.txt", 500),
        ("large.txt", 1000),
        ("tiny.txt", 50),
        ("huge.txt", 2000),
    ]
    
    created_files = []
    for filename, size in files_data:
        file_path = tmp_path / filename
        file_path.write_bytes(b"x" * size)
        created_files.append((file_path, size))
    
    # Test: get top 3 largest
    result = largest_files(tmp_path, n=3)
    
    assert len(result) == 3
    assert result[0].size_bytes == 2000
    assert result[1].size_bytes == 1000
    assert result[2].size_bytes == 500
    
    # Verify FileInfo objects
    assert all(isinstance(fi, FileInfo) for fi in result)
    assert all(fi.path.is_absolute() for fi in result)


def test_largest_files_n_greater_than_count(tmp_path):
    """
    Test largest_files with n > file count.
    
    Returns all files without error.
    """
    # Create 3 files
    for i, size in enumerate([100, 200, 300]):
        (tmp_path / f"file_{i}.txt").write_bytes(b"x" * size)
    
    # Request more files than exist
    result = largest_files(tmp_path, n=10)
    
    assert len(result) == 3
    assert result[0].size_bytes == 300
    assert result[1].size_bytes == 200
    assert result[2].size_bytes == 100


def test_files_to_free_space_exact_threshold(tmp_path):
    """
    Test files_to_free_space with exact threshold.
    
    Target equals sum of selected files.
    Verify minimal number of files returned.
    """
    # Create files with known sizes
    files_data = [
        ("file1.txt", 100),
        ("file2.txt", 200),
        ("file3.txt", 300),
        ("file4.txt", 400),
    ]
    
    for filename, size in files_data:
        (tmp_path / filename).write_bytes(b"x" * size)
    
    # Target: 500 bytes (should get file4 + file3 = 400 + 300 = 700)
    result = files_to_free_space(tmp_path, target_bytes=500)
    
    assert len(result) == 2
    total = sum(f.size_bytes for f in result)
    assert total >= 500
    assert result[0].size_bytes == 400
    assert result[1].size_bytes == 300
    
    # Verify minimal: can't free 500 with just the largest file
    assert len(result) == 2


def test_files_to_free_space_exceeding_total(tmp_path):
    """
    Test files_to_free_space with target exceeding total size.
    
    Target larger than total directory size.
    Verify all files returned.
    """
    # Create files
    files_data = [
        ("file1.txt", 100),
        ("file2.txt", 200),
    ]
    
    for filename, size in files_data:
        (tmp_path / filename).write_bytes(b"x" * size)
    
    # Target larger than total (100 + 200 = 300)
    result = files_to_free_space(tmp_path, target_bytes=1000)
    
    assert len(result) == 2
    total = sum(f.size_bytes for f in result)
    assert total == 300


def test_files_to_free_space_zero_or_negative_target(tmp_path):
    """
    Test files_to_free_space with zero or negative target.
    
    Verify empty list returned.
    """
    # Create some files
    (tmp_path / "file1.txt").write_bytes(b"x" * 100)
    
    # Test zero target
    result_zero = files_to_free_space(tmp_path, target_bytes=0)
    assert result_zero == []
    
    # Test negative target
    result_negative = files_to_free_space(tmp_path, target_bytes=-100)
    assert result_negative == []

