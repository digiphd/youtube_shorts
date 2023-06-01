import shutil
import os

def create_temp_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def remove_temp_folder(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)