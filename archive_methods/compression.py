import os
import zipfile
import ui.MainWindow

total_files_compressed = 0
total_files_n_compressed = 0
progress_bar = 0


def compress_files_and_folders(folder, archive_name, filename_list, folders_name_list, number_of_files, progress_bar_w,
                               compress_type=zipfile.ZIP_DEFLATED):
    global total_files_compressed, total_files_n_compressed, progress_bar
    if folder is not None:
        progress_bar = progress_bar_w
        total_files_n_compressed = number_of_files
        path = os.path.join(folder, archive_name)
        new_zip = zipfile.ZipFile(path, 'w')
        compress_files(new_zip, filename_list, compress_type)
        compress_subfolders(new_zip, folders_name_list, compress_type)
        new_zip.close()


def compress_files(archive, filename_list, compress_type=zipfile.ZIP_DEFLATED):
    global total_files_compressed, total_files_n_compressed, progress_bar
    for filename in filename_list:
        archive.write(filename, compress_type=compress_type)
        total_files_compressed += 1
        progress_bar.setProperty("value", total_files_compressed/total_files_n_compressed * 100)


def compress_subfolders(archive, folders_list, compress_type=zipfile.ZIP_DEFLATED):
    for kit in folders_list:
        filename_list = []
        for i in kit[2]:
            filename_list.append(str(kit[0] + '/' + i))
        compress_files(archive, filename_list, compress_type)
