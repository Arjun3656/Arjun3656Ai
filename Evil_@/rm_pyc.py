import os
import shutil

def remove_pycache(path):
    """Removes all __pycache__ folders recursively from the given path."""

    for root, dirs, files in os.walk(path):
        if "__pycache__" in dirs:
            shutil.rmtree(os.path.join(root, "__pycache__"))

# Example usage:
remove_pycache(".")  # Removes all __pycache__ folders in the current directory and its subdirectories