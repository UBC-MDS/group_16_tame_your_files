import pytest
import os
from tame_your_files.visualize_dir import get_directory_data, create_treemap_figure

# LLM Transparency: Gemini 3 was used to assist in drafting these unit tests. The tests were manually reviewed. 

@pytest.fixture
def mock_dir(tmp_path):
    """
    Creates a dummy directory structure:
    root/
      - file1.txt (5 bytes)
      - sub/
        - file2.txt (10 bytes)
    """
    root = tmp_path / "root"
    root.mkdir()
    (root / "file1.txt").write_text("12345") # 5 bytes
    
    sub = root / "sub"
    sub.mkdir()
    (sub / "file2.txt").write_text("1234567890") # 10 bytes
    
    return root

def test_data_discovery_count(mock_dir):
    """
    Verifies that every file and folder is accounted for.
    """
    data = get_directory_data(str(mock_dir))
    # Expecting root, file1, sub, file2 = 4 items
    assert len(data) == 4, "Should discover all files and directories"

def test_data_hierarchy_links(mock_dir):
    """
    Verifies that children correctly point to their parent directory.
    """
    data = get_directory_data(str(mock_dir))
    sub_dir_path = str(mock_dir / "sub")
    file2_path = str(mock_dir / "sub" / "file2.txt")
    
    file2_entry = next(item for item in data if item["id"] == file2_path)
    assert file2_entry["parent"] == sub_dir_path, "File in subfolder must point to subfolder as parent"

def test_data_size_accuracy(mock_dir):
    """
    Verifies the os.getsize integration is accurate.
    """
    data = get_directory_data(str(mock_dir))
    file1_path = str(mock_dir / "file1.txt")
    
    file1_entry = next(item for item in data if item["id"] == file1_path)
    assert file1_entry["value"] == 5, "File size should match the number of characters/bytes"
    
def test_get_directory_data_invalid_path():
    """
    Ensure it raises FileNotFoundError for bad paths.
    """
    with pytest.raises(FileNotFoundError):
        get_directory_data("/non/existent/path/at/all")

def test_create_treemap_figure_type(mock_dir):
    """
    Verify that the figure helper returns a Plotly Figure object.
    """
    import plotly.graph_objects as go
    data = get_directory_data(str(mock_dir))
    fig = create_treemap_figure(data)
    
    # Checking if output is a valid figure
    assert isinstance(fig, go.Figure)