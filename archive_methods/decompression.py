import os.path
import zipfile


def extract_all(zipfile_dir, extract_dir):
    file = zipfile.ZipFile(zipfile_dir)
    file.extractall(extract_dir)
    file.close()



def extract_one(zipfile_dir, filename, extract_dir):
    if not zipfile_dir[:-3] == 'zip': return
    file = zipfile.ZipFile(zipfile_dir)
    file.extract(filename, extract_dir)
    file.close()
