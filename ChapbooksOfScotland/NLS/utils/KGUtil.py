import os
from os import listdir
from os.path import isdir, join, dirname, realpath
from pathlib import Path


def create_nls_folder_path_mapping_file(result_filename, nls_data_folder_path):
    # Read nls data folder and store volume name
    dirs = [f for f in listdir(nls_data_folder_path) if isdir(join(nls_data_folder_path, f))]
    print(dirs)

    # Write volume paths to result file.
    result_file = open(result_filename, 'w')
    for folder_name in dirs:
        result_file.write(join(nls_data_folder_path, folder_name) + '\n')
    pass


if __name__ == '__main__':
    parent_path = Path(os.path.abspath(os.path.dirname(__file__))).parent.absolute()
    chapbook_data_mapping_file_path = str(parent_path) + '/chapbook.txt'
    chapbook_data_file_path = '/Users/ly40/Downloads/nls-data-chapbooks'
    create_nls_folder_path_mapping_file(chapbook_data_mapping_file_path, chapbook_data_file_path)
