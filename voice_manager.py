import common_tools
import os
from scipy.io import wavfile

ALLOWED_VOICE_EXTENSIONS = set(['wav', 'WAV'])

VOICE_FILE_TAIL = '.wav'


class VoiceManager:
    def __init__(self):
        self.voice_path = "./data/voices/"
        self.common_voices = common_tools.get_folder_file_list(self.voice_path + 'common', VOICE_FILE_TAIL)

    def add_voice(self, voice_file, voice_tag):
        if voice_file and VoiceManager.allowed_file(voice_file.filename):
            new_voice_id = common_tools.get_new_id("voice", voice_tag)
            filename = str(new_voice_id) + VOICE_FILE_TAIL
            voice_folder_path = self.voice_path + voice_tag + '/'
            common_tools.check_and_build_folder(voice_folder_path)
            voice_file.save(os.path.join(voice_folder_path, filename))
            return new_voice_id
        return ''

    def get_voice(self, voice_id):
        voice_local_path = common_tools.get_id_folder(voice_id)
        voice_local_file_name = self.voice_path + voice_local_path + voice_id + VOICE_FILE_TAIL
        if os.path.exists(voice_local_file_name):
            sample_rate, voice_data = wavfile.read(self.voice_path + voice_local_path + voice_id + VOICE_FILE_TAIL)
            return sample_rate, voice_data
        return None, None

    def get_voice_raw(self, voice_id):
        voice_local_path = common_tools.get_id_folder(voice_id)
        voice_local_file_name = self.voice_path + voice_local_path + voice_id + VOICE_FILE_TAIL
        if os.path.exists(voice_local_file_name):
            with open(voice_local_file_name, 'rb') as f:
                voice_raw = f.read()
            return voice_raw
        return None

    def get_voice_list(self, voice_tag):
        voice_list = self.common_voices
        voice_list += common_tools.get_folder_file_list(self.voice_path + voice_tag, VOICE_FILE_TAIL)
        return voice_list

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_VOICE_EXTENSIONS