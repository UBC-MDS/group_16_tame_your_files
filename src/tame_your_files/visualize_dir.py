"""
This script provides functions to visualize the directory structure of a given path.

To facilitate testing, the main function `visualize_directory` calls two functions with returnable outputs: `build_directory_tree` and `format_tree_output`.


Author: Jeffrey Ding
""" 
import os
import plotly.express as px
import plotly.graph_objects as go

def get_directory_data(target_path):
    """
    Walks the directory and builds a representative list of dictionaries of all children. Uses os.walk to capture every file and folder.

    Parameters
    ----------
    target_path : str
        The root directory path from which to start building the data.
    
    Returns
    -------
    list of dict
        A list of dictionaries representing files and folders with their sizes and hierarchy.
    """
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Path not found: {target_path}")

    data = []
    # Normalize path to ensure consistency
    target_path = os.path.abspath(target_path)
    
    for root, dirs, files in os.walk(target_path):
        # Add current directory
        parent = os.path.dirname(root) if root != target_path else ""
        
        # Folder Entry
        data.append({
            "id": root,
            "name": os.path.basename(root),
            "parent": parent,
            "value": 0 # Folders accumulate size from children in Plotly
        })
        
        # File Entries
        for f in files:
            f_path = os.path.join(root, f)
            try:
                f_size = os.path.getsize(f_path)
            except OSError:
                f_size = 0 # Handle system files/permissions
                
            data.append({
                "id": f_path,
                "name": f,
                "parent": root,
                "value": f_size
            })
            
    return data

def create_treemap_figure(data):
    """
    Transforms the flat list into a Plotly Treemap object.

    Parameters
    ----------  
    data : list of dict
        The list of dictionaries representing files and folders with their sizes and hierarchy.
    
    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly Treemap figure representing the directory structure.
    """
    ids = [item["id"] for item in data]
    labels = [item["name"] for item in data]
    parents = [item["parent"] for item in data]
    values = [item["value"] for item in data]

    fig = go.Figure(go.Treemap(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total", # Important: ensures folder size = sum of children
        hovertemplate='<b>%{label}</b><br>Size: %{value} bytes<extra></extra>'
    ))
    
    fig.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    return fig

def visualize_dir(path="."):
    """
    Main function to visualize the directory.

    Parameters
    ----------
    path : str, default="."
        The root directory path from which to start visualizing the directory structure.
    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly Treemap figure representing the directory structure.
    """

    data = get_directory_data(path)
    fig = create_treemap_figure(data)
    return fig

if __name__ == "__main__":
    # Example usage:
    fig = visualize_dir(".")
    fig.show()