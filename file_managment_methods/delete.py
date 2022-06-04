import os
from shutil import rmtree

def delete_archive(path):
    if path[:-3] != "zip": return
    os.remove(path)


def delete_file(filename_list, folders_list):
    filename_list = filename_list[0]
    for path in filename_list:
        print(path)
        os.remove(path)
    for path in folders_list:
        rmtree(path, ignore_errors=True)
