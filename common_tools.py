import datetime
import os


def get_folder_file_list(folder_path, file_tail):
    file_list = []
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1] == file_tail:
                    file_list.append(os.path.splitext(file)[0])
    return file_list


def check_and_build_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_new_id(id_header, id_tag):
    id_str = id_header + '_' + id_tag + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return id_str


def get_id_folder(id_str):
    id_params = id_str.split('_')
    if len(id_params) > 2:
        return id_params[1] + '/'
    else:
        return ''
