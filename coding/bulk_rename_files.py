# filename: bulk_rename_files.py

import os

path = "/path/to/folder/"
prefix = "Prefix"

files = os.listdir(path)
files.sort(key=os.path.getctime)

index = 1
for file in files:
    _, ext = os.path.splitext(file)
    new_name = f"{prefix}_{index:03}{ext}"
    os.rename(os.path.join(path, file), os.path.join(path, new_name))
    index += 1