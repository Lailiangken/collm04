import os
import stat

def is_readable_directory(path):
    try:
        mode = os.stat(path).st_mode
        if stat.S_ISDIR(mode) and os.access(path, os.R_OK):
            return True
    except FileNotFoundError:
        pass
    return False

folder_path = "実際のフォルダパスを指定"

if is_readable_directory(folder_path):
    print("Folder is readable.")
else:
    print("Folder is not accessible or does not exist.")