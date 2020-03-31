from flask import Flask
from flask import request
from flask import abort
from flask import Response
from flask import render_template
from photo_manager import PhotoManager
from voice_manager import VoiceManager
import json

app = Flask(__name__)

photo_manager = PhotoManager()
voice_manager = VoiceManager()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload/photo', methods=['POST'])
def upload_photo():
    photo_tag = request.args.get('user')
    photo_file = request.files['file']  # 获取上传的文件
    photo_id = photo_manager.add_photo(photo_file, photo_tag)
    if photo_id == '':
        abort(415)
    rt = {'photo_id': photo_id}
    return Response(json.dumps(rt), mimetype='application/json')


@app.route('/upload/voice', methods=['POST'])
def upload_voice():
    voice_tag = request.args.get('user')
    voice_file = request.files['file']  # 获取上传的文件
    voice_id = photo_manager.add_photo(voice_file, voice_tag)
    if voice_id == '':
        abort(415)
    rt = {'voice_id': voice_id}
    return Response(json.dumps(rt), mimetype='application/json')


@app.route('/process', methods=['POST'])
def process():
    photo_id = request.args.get('photo_id')
    voice_id = request.args.get('voice_id')
    photo_data = photo_manager.get_photo(photo_id)
    sample_rate, voice_data = voice_manager.get_voice(voice_id)
    if photo_data is None or sample_rate is None:
        abort(404)
    # TODO use photo data and voice data to process result
    photo_raw = photo_manager.get_photo_raw(photo_id)
    return Response(photo_raw, mimetype='image/png')


@app.route('/photo/list', methods=['GET'])
def photo_list():
    photo_tag = request.args.get('user')
    photo_list_data = photo_manager.get_photo_list(photo_tag)
    rt = {'photo_list': photo_list_data}
    return Response(json.dumps(rt), mimetype='application/json')


@app.route('/photo/<photo_id>', methods=['GET'])
def photo_get(photo_id):
    photo_raw = photo_manager.get_photo_raw(photo_id)
    if photo_raw is None:
        abort(404)
    return Response(photo_raw, mimetype='image/png')


@app.route('/voice/list', methods=['GET'])
def voice_list():
    voice_tag = request.form['user']
    voice_list_data = voice_manager.get_voice_list(voice_tag)
    rt = {'voice_list': voice_list_data}
    return Response(json.dumps(rt), mimetype='application/json')


@app.route('/voice/<voice_id>', methods=['GET'])
def voice_get(voice_id):
    voice_raw = voice_manager.get_voice_raw(voice_id)
    if voice_raw is None:
        abort(404)
    return Response(voice_raw, mimetype='audio/x-wav')


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run()
