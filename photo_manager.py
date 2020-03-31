import cv2
import common_tools
import os
from werkzeug.utils import secure_filename

ALLOWED_PHOTO_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])

PHOTO_FILE_TAIL = '.png'


class PhotoManager:
    def __init__(self):
        self.photo_path = "./data/photos/"
        self.photo_temp_path = "./data/photos/temp/"
        self.common_photos = common_tools.get_folder_file_list(self.photo_path + 'common', PHOTO_FILE_TAIL)

    def add_photo(self, photo_file, photo_tag):
        if photo_file and PhotoManager.allowed_file(photo_file.filename):  # 如果文件存在并且符合要求则为 true
            new_photo_id = common_tools.get_new_id("photo", photo_tag)
            photo_folder_path = self.photo_path + photo_tag + '/'
            common_tools.check_and_build_folder(photo_folder_path)
            filename = secure_filename(photo_file.filename)  # 获取上传文件的文件名
            photo_file.save(os.path.join(self.photo_temp_path, filename))  # 保存文件
            photo_cvmat = cv2.imread(os.path.join(self.photo_temp_path, filename))
            cv2.imwrite(photo_folder_path + str(new_photo_id) + PHOTO_FILE_TAIL, photo_cvmat)
            os.remove(os.path.join(self.photo_temp_path, filename))
            return new_photo_id
        return ''

    def get_photo(self, photo_id):
        photo_local_path = common_tools.get_id_folder(photo_id)
        photo_file_name = self.photo_path + photo_local_path + photo_id + PHOTO_FILE_TAIL
        if os.path.exists(photo_file_name):
            photo_data = cv2.imread(photo_file_name)
            return photo_data
        return None

    def get_photo_raw(self, photo_id):
        photo_local_path = common_tools.get_id_folder(photo_id)
        photo_local_file_name = self.photo_path + photo_local_path + photo_id + PHOTO_FILE_TAIL
        if os.path.exists(photo_local_file_name):
            with open(photo_local_file_name, 'rb') as f:
                photo_raw = f.read()
            return photo_raw
        return None

    def get_photo_list(self, photo_tag):
        photo_list = self.common_photos.copy()
        photo_list += common_tools.get_folder_file_list(self.photo_path + photo_tag, PHOTO_FILE_TAIL)
        return photo_list

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_PHOTO_EXTENSIONS