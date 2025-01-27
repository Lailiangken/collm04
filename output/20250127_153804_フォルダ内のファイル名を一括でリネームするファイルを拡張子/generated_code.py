# filename: rename_files.py
import os
import shutil
from datetime import datetime

def rename_files(prefix, path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    
    ext_dict = {}
    for f in files:
        _, ext = os.path.splitext(f)
        ext = ext[1:]
        if ext not in ext_dict:
            ext_dict[ext] = []
        ext_dict[ext].append(f)
    
    for ext, file_list in ext_dict.items():
        ext_folder = os.path.join(path, ext)
        os.makedirs(ext_folder, exist_ok=True)
        for i, filename in enumerate(file_list):
            new_name = f"{prefix}_{i+1}.{ext}"
            new_path = os.path.join(ext_folder, new_name)
            shutil.move(os.path.join(path, filename), new_path)

prefix = "my_files"
path = "/path/to/your/folder"  # Update this line with the actual folder path
rename_files(prefix, path)