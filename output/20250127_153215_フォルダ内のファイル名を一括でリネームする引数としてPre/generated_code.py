# filename: batch_file_rename.py
import os
from datetime import datetime

def batch_file_rename(prefix, path):
    files = os.listdir(path)
    files.sort(key=lambda x: os.path.getctime(os.path.join(path, x)))
    for i, filename in enumerate(files, start=1):
        _, ext = os.path.splitext(filename)
        new_name = f"{prefix}_{i}{ext}"
        os.rename(os.path.join(path, filename), os.path.join(path, new_name))

# Usage
batch_file_rename("newfile", "/actual/path/to/folder")