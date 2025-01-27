# filename: list_files.py
import os

folder_path = "/path/to/folder"
files = os.listdir(folder_path)

for file in files:
    print(file)