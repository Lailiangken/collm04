# filename: list_files.py
import os

folder_path = "/Users/username/Documents"
files = os.listdir(folder_path)

for file in files:
    print(file)