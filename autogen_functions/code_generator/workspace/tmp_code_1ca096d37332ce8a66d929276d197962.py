import os

def rename_files_in_folder(folder_path, prefix):
    files = os.listdir(folder_path)
    files.sort(key=os.path.getmtime)
    
    for idx, file_name in enumerate(files):
        file_ext = os.path.splitext(file_name)[-1]
        new_file_name = f"{prefix}_{idx+1:03}{file_ext}"
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))

# フォルダパスとプレフィックスを設定する
folder_path = 'ここにフォルダの絶対パスを入力'
prefix = 'ここにプレフィックスを入力'

rename_files_in_folder(folder_path, prefix)