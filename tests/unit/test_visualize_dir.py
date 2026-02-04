import pytest
import plotly.graph_objects as go
from tame_your_files.visualize_dir import (
    get_directory_data,
    create_treemap_figure,
    visualize_dir,
)

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
    (root / "file1.txt").write_text("12345")  # 5 bytes

    sub = root / "sub"
    sub.mkdir()
    (sub / "file2.txt").write_text("1234567890")  # 10 bytes

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
    assert file2_entry["parent"] == sub_dir_path, (
        "File in subfolder must point to subfolder as parent"
    )


def test_data_size_accuracy(mock_dir):
    """
    Verifies the os.getsize integration is accurate.
    """
    data = get_directory_data(str(mock_dir))
    file1_path = str(mock_dir / "file1.txt")

    file1_entry = next(item for item in data if item["id"] == file1_path)
    assert file1_entry["value"] == 5, (
        "File size should match the number of characters/bytes"
    )


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

    data = get_directory_data(str(mock_dir))
    fig = create_treemap_figure(data)

    # Checking if output is a valid figure
    assert isinstance(fig, go.Figure)


def test_visualize_dir_empty_directory(tmp_path):
    """
    Test visualization of an empty directory.
    """

    # Create an empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    # Get data
    data = get_directory_data(str(empty_dir))

    # Should contain only the root entry
    assert len(data) == 1
    assert data[0]["name"] == "empty"
    assert data[0]["value"] == 0

    # Should produce a valid figure
    fig = visualize_dir(str(empty_dir))
    assert isinstance(fig, go.Figure)


def test_visualize_dir_only_subdirectories(tmp_path):
    """
    Test visualization of a directory containing only subdirectories.
    """
    root = tmp_path / "root"
    root.mkdir()
    (root / "sub1").mkdir()
    (root / "sub2").mkdir()

    data = get_directory_data(str(root))

    # Root + 2 subdirs = 3 entries
    assert len(data) == 3
    names = [item["name"] for item in data]
    assert "sub1" in names
    assert "sub2" in names


def test_visualize_dir_main_function(tmp_path):
    """
    Test the main visualize_dir function integration.
    """

    root = tmp_path / "root"
    root.mkdir()
    (root / "file.txt").write_text("content")

    fig = visualize_dir(str(root))

    assert isinstance(fig, go.Figure)
    # Check if data is present in the figure
    assert len(fig.data) > 0
    assert isinstance(fig.data[0], go.Treemap)


def test_get_directory_data_permission_error(tmp_path):
    """
    Test handling of permission errors during file size access.
    """
    from unittest.mock import patch

    # Setup mock structure
    root = str(tmp_path)

    with patch("os.walk") as mock_walk:
        mock_walk.return_value = [(root, [], ["protected_file.txt"])]

        # Mock os.path.getsize to raise OSError
        with patch("os.path.getsize", side_effect=OSError("Permission denied")):
            data = get_directory_data(root)

            # Should still process the file but with size 0
            file_entry = next(
                item for item in data if item["name"] == "protected_file.txt"
            )
            assert file_entry["value"] == 0


def test_visualize_dir_default_path(tmp_path):
    """
    Test visualize_dir with default argument (current directory).
    We change the current working directory to tmp_path to avoid scanning the entire project.
    """
    import os

    # Create some content in tmp_path
    (tmp_path / "default.txt").write_text("default content")

    # Change CWD safely
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        # Call without arguments
        fig = visualize_dir()
        assert isinstance(fig, go.Figure)

        # Option 1: Convert to tuple first (type-safe)
        assert len(tuple(fig.data)) > 0

        # Option 2: Check the attribute exists instead
        # assert hasattr(fig, 'data') and fig.data
    finally:
        os.chdir(original_cwd)
