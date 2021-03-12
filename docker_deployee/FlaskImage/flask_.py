from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response
import time
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/test')
def test():
    return "test3 ~"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/has_guest_since/<int:lgct>', methods=['GET'])
def has_guest_since(lgct):
    mtime = int(os.path.getmtime('./upload/guest_photo.jpg')) #檔案上次修改的時間
    if(lgct < mtime):
        return jsonify(True)
    else:
        return jsonify(False)

@app.route('/uploaded/guest', methods=['POST'], strict_slashes=False)
def api_upload_guest():
    fff = request.files['myFile']
    fff.save("./upload/guest_photo.jpg")
    return jsonify({"success": 0, "msg": "upload successful!"})

# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open("./upload/" + filename, "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

# # 上傳檔案範例
# @app.route('/upload')
# def page_upload():
#     return render_template('upload.html')

# # 上傳檔案範例
# @app.route('/uploaded', methods=['POST'], strict_slashes=False)
# def api_uploaded():
#     fff = request.files['myFile']
#     print(type(fff))
#     org_fname = secure_filename(fff.filename)
#     print("org_fname: ", org_fname)
#     new_fname = str(int(time.time())) + '.' + org_fname.rsplit('.', 1)[1]
#     print("new_fname: ", new_fname)
#     fff.save("./upload/" + new_fname)
#     return jsonify({"success": 0, "msg": "upload successful!"})

if __name__ == "__main__":
        # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8888)
