# Deprecated...

from flask import Flask, render_template, jsonify, request, make_response, abort
import face_detection
import requests


app = Flask(__name__)

# 上傳使用者的新相片
@app.route('/', methods=['POST'], strict_slashes=False)
def face():
    fff = request.files['myFile']
    fff.save("./input.jpg")
    result = face_detection.face_detect('./input.jpg')
    if (result):
        requests.get('https://khaos.tw/open_door/5')
    return jsonify(result)

# 註冊新的使用者
@app.route('/reg', methods=['POST'], strict_slashes=False)
def face():
    fff = request.files['myFile']
    fff.save("./input.jpg")
    result = face_detection.face_detect('./input.jpg')
    if (result):
        requests.get('https://khaos.tw/open_door/5')
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50000)