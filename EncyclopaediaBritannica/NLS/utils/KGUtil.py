from os import listdir
from os.path import isdir, join, dirname, realpath


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
    NLS_path = '/Users/ly40/Documents/PhD/InformationExtraction/EncyclopaediaBritannica/NLS'
    eb_data_mapping_file_path = NLS_path + '/eb.txt'
    eb_data_file_path = NLS_path + '/nls-data-encyclopaediaBritannica'
    create_nls_folder_path_mapping_file(eb_data_mapping_file_path, eb_data_file_path)
