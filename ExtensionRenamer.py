import os
from Qt import QtWidgets

def preprocess_textures(path):
    """Analyzes textures in folder to determine if their extension is correct"""
    count = 0

    if os.path.isdir(path):

        for (dirpath, directory_paths, file_names) in os.walk(path):
            for file_name in file_names:
                if file_name.endswith('.targa') or file_name.endswith('.TGA'):

                    print file_name
                    base_file, ext = os.path.splitext(file_name)
                    print base_file
                    print type(base_file)
                    original_file_name_path = os.path.join(
                        dirpath, file_name)
                    print original_file_name_path
                    new_file_name_path = os.path.join(
                        dirpath, base_file + '.tga')
                    # in order to successfully rename a file
                    # the file needs to be joined with the path
                    os.rename(original_file_name_path, new_file_name_path)
                    list_of_files[file_name] = os.sep.join(
                        [dirpath, file_name])
                    count += 1
        if count == 0:
            title = 'No Files Found'
            message = 'There were not any files that needed their extensions formatted'
            QtWidgets.QMesssageBox(title, message)
        else:
            title = 'Completed File Renaming'
            message = str(count) + 'Files had their extenstions changed to .tga'
    else:
        title = 'Cannot Proceed'
        message = 'Invalid Path Provided'

    QtWidgets.QMesssageBox(title, message)
