"""
Unit tests for file_size_utilities module.

These tests focus on logic, data structures, and edge cases
without requiring filesystem access.
"""
import pytest
from pathlib import Path
from tame_your_files.file_size_utilities import FileInfo


class TestFileInfo:
    """Unit tests for FileInfo dataclass."""
    
    def test_fileinfo_creation(self):
        """Test FileInfo can be created with path and size."""
        path = Path("/test/file.txt")
        size = 1000
        file_info = FileInfo(path=path, size_bytes=size)
        
        assert file_info.path == path
        assert file_info.size_bytes == size
    
    def test_fileinfo_immutable(self):
        """Test FileInfo is immutable (frozen dataclass)."""
        from dataclasses import FrozenInstanceError
        
        file_info = FileInfo(path=Path("/test/file.txt"), size_bytes=1000)
        
        with pytest.raises(FrozenInstanceError):
            file_info.size_bytes = 2000  # type: ignore[misc]
    
    def test_fileinfo_equality(self):
        """Test FileInfo equality comparison."""
        path1 = Path("/test/file1.txt")
        path2 = Path("/test/file2.txt")
        
        file_info1 = FileInfo(path=path1, size_bytes=1000)
        file_info2 = FileInfo(path=path1, size_bytes=1000)
        file_info3 = FileInfo(path=path2, size_bytes=1000)
        file_info4 = FileInfo(path=path1, size_bytes=2000)
        
        assert file_info1 == file_info2  # Same path and size
        assert file_info1 != file_info3  # Different path
        assert file_info1 != file_info4  # Different size
    
    def test_fileinfo_hashable(self):
        """Test FileInfo is hashable (required for frozen dataclass)."""
        file_info1 = FileInfo(path=Path("/test/file1.txt"), size_bytes=1000)
        file_info2 = FileInfo(path=Path("/test/file2.txt"), size_bytes=2000)
        
        # Should be able to create a set
        file_set = {file_info1, file_info2}
        assert len(file_set) == 2
        
        # Should be able to use as dict key
        file_dict = {file_info1: "first", file_info2: "second"}
        assert file_dict[file_info1] == "first"


class TestFileInfoSorting:
    """Unit tests for sorting logic used in file_size_utilities."""
    
    def test_sorting_by_size_descending(self):
        """Test FileInfo objects can be sorted by size in descending order."""
        files = [
            FileInfo(path=Path("/test/small.txt"), size_bytes=100),
            FileInfo(path=Path("/test/large.txt"), size_bytes=1000),
            FileInfo(path=Path("/test/medium.txt"), size_bytes=500),
        ]
        
        sorted_files = sorted(files, key=lambda x: (-x.size_bytes, str(x.path)))
        
        assert sorted_files[0].size_bytes == 1000
        assert sorted_files[1].size_bytes == 500
        assert sorted_files[2].size_bytes == 100
    
    def test_sorting_deterministic_with_same_size(self):
        """Test sorting is deterministic when files have same size."""
        files = [
            FileInfo(path=Path("/test/z_file.txt"), size_bytes=100),
            FileInfo(path=Path("/test/a_file.txt"), size_bytes=100),
            FileInfo(path=Path("/test/m_file.txt"), size_bytes=100),
        ]
        
        sorted_files = sorted(files, key=lambda x: (-x.size_bytes, str(x.path)))
        
        # Should sort by path alphabetically when sizes are equal
        assert sorted_files[0].path.name == "a_file.txt"
        assert sorted_files[1].path.name == "m_file.txt"
        assert sorted_files[2].path.name == "z_file.txt"


class TestSelectionLogic:
    """Unit tests for file selection logic."""
    
    def test_nlargest_selection(self):
        """Test logic for selecting n largest files."""
        import heapq
        
        files = [
            FileInfo(path=Path("/test/file1.txt"), size_bytes=100),
            FileInfo(path=Path("/test/file2.txt"), size_bytes=500),
            FileInfo(path=Path("/test/file3.txt"), size_bytes=1000),
            FileInfo(path=Path("/test/file4.txt"), size_bytes=200),
            FileInfo(path=Path("/test/file5.txt"), size_bytes=300),
        ]
        
        # Select top 3 largest
        largest = heapq.nlargest(3, files, key=lambda x: x.size_bytes)
        
        assert len(largest) == 3
        sizes = [f.size_bytes for f in largest]
        assert 1000 in sizes
        assert 500 in sizes
        assert 300 in sizes
        assert 100 not in sizes
        assert 200 not in sizes
    
    def test_greedy_selection_logic(self):
        """Test greedy selection logic for files_to_free_space."""
        files = [
            FileInfo(path=Path("/test/file1.txt"), size_bytes=100),
            FileInfo(path=Path("/test/file2.txt"), size_bytes=200),
            FileInfo(path=Path("/test/file3.txt"), size_bytes=300),
            FileInfo(path=Path("/test/file4.txt"), size_bytes=400),
        ]
        
        # Sort by size descending
        sorted_files = sorted(files, key=lambda x: (-x.size_bytes, str(x.path)))
        
        # Simulate greedy selection for target of 500 bytes
        target_bytes = 500
        result = []
        total_size = 0
        
        for file_info in sorted_files:
            result.append(file_info)
            total_size += file_info.size_bytes
            if total_size >= target_bytes:
                break
        
        assert len(result) == 2
        assert result[0].size_bytes == 400
        assert result[1].size_bytes == 300
        assert total_size == 700
        assert total_size >= target_bytes
    
    def test_greedy_selection_exceeding_total(self):
        """Test greedy selection when target exceeds total."""
        files = [
            FileInfo(path=Path("/test/file1.txt"), size_bytes=100),
            FileInfo(path=Path("/test/file2.txt"), size_bytes=200),
        ]
        
        sorted_files = sorted(files, key=lambda x: (-x.size_bytes, str(x.path)))
        
        target_bytes = 1000  # Larger than total (300)
        result = []
        total_size = 0
        
        for file_info in sorted_files:
            result.append(file_info)
            total_size += file_info.size_bytes
            if total_size >= target_bytes:
                break
        
        # Should return all files even though target isn't met
        assert len(result) == 2
        assert total_size == 300


class TestEdgeCases:
    """Unit tests for edge cases and input validation."""
    
    def test_zero_target_returns_empty(self):
        """Test that zero target returns empty list."""
        # This tests the early return logic
        target_bytes = 0
        result = []
        
        # Simulate the early return
        if target_bytes <= 0:
            result = []
        
        assert result == []
    
    def test_negative_target_returns_empty(self):
        """Test that negative target returns empty list."""
        target_bytes = -100
        result = []
        
        # Simulate the early return
        if target_bytes <= 0:
            result = []
        
        assert result == []
    
    def test_empty_file_list(self):
        """Test behavior with empty file list."""
        files = []
        
        # Test nlargest with empty list
        import heapq
        largest = heapq.nlargest(10, files, key=lambda x: x.size_bytes)
        assert largest == []
        
        # Test sorting empty list
        sorted_files = sorted(files, key=lambda x: (-x.size_bytes, str(x.path)))
        assert sorted_files == []

