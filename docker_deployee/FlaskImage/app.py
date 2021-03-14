from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, abort
import time
import os
import datetime
import sqlite3
import requests
import json
import cv2
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


CHANNEL_ACCESS_TOKEN = 'QeKanfGknXD8gNkDfj7uwbhvzSEeyFMtSEvXuJqQSrAf19m6QF/bThdIoyBXQ2DoSKzp5wxcl5+KrmoOjVCpAVO4MNw5DGUWF+v5ftpcHEXGzkkSYqA5hmguvYmIgTWG126nF9VL1vwA3hp4JM3PGgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'c545b95334594c4f6a8814ef668f45af'
USER_ID = 'U93d26f445d8c2de9676b9467a69ae33e'

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def index():
    return render_template('index.html')

# 初始化資料庫
@app.route('/sql_init')
def sql_init():
    conn = sqlite3.connect('iot.db')
    c = conn.cursor()
    # 建立表格
    c.execute('''create table if not exists STATUS
        (KEY    TEXT    NOT NULL,
        VALUE   TEXT    NOT NULL,
        PRIMARY KEY (KEY));
        ''')
    # 插入資料 (若不存在的話)
    cc = c.execute("SELECT * FROM STATUS WHERE KEY = 'Locked';")
    entry = cc.fetchone()
    if entry is None:  # 'No entry found'
        c.execute("INSERT INTO STATUS (KEY,VALUE) \
            VALUES ('Locked', 'yes' )")
    conn.commit()
    conn.close()
    return jsonify("OK")

# 開門t秒 ->應搭配身分認證
@app.route('/open_door/<int:t>', methods=['GET'])
def open_door(t):
    conn = sqlite3.connect('iot.db')
    c = conn.cursor()
    c.execute("UPDATE STATUS SET \
                VALUE = 'no' where KEY = 'Locked'")  # 門是開的
    conn.commit()
    conn.close()

    time.sleep(t)

    conn = sqlite3.connect('iot.db')
    c = conn.cursor()
    c.execute("UPDATE STATUS SET \
                VALUE = 'yes' where KEY = 'Locked'")  # 門是關的
    conn.commit()
    conn.close()
    return jsonify("OK")

# 確認門現在是開的還是關的
@app.route('/door_status')
def door_status():
    conn = sqlite3.connect('iot.db')
    c = conn.cursor()
    cc = c.execute("SELECT VALUE FROM STATUS WHERE KEY = 'Locked'")
    result = cc.fetchone()[0]
    conn.commit()
    conn.close()
    if(result == 'yes'):
        return jsonify(True)  # 門是關的
    else:
        return jsonify(False)  # 門是開的

# 根據給定的時間 判斷是否有新的訪客過來
@app.route('/has_guest_since/<int:lgct>', methods=['GET'])
def has_guest_since(lgct):
    mtime = int(os.path.getmtime('./upload/guest_photo.jpg'))  # 檔案上次修改的時間
    if(lgct < mtime):
        return jsonify(True)
    else:
        return jsonify(False)

# 上傳使用者的新相片
@app.route('/uploaded/guest', methods=['POST'], strict_slashes=False)
def api_upload_guest():
    fff = request.files['myFile']
    fff.save("./upload/guest_photo.jpg")
    # 縮小圖片
    image = cv2.imread("./upload/guest_photo.jpg")
    h, w, channels = image.shape

    if (w > h):
        image = cv2.resize(image, (300, int(300*h/w)), interpolation=cv2.INTER_AREA)
    else:
        image = cv2.resize(image, (int(300*w/h), 300), interpolation=cv2.INTER_AREA)

    cv2.imwrite('./upload/guest_photo_.jpg', image)

    # LINE BOT 通知
    lineHeader = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN
    }
    # LINE BOT 通知 > 文字提示+照片
    lineData = {
        'messages': [
            {
                "type": "text",
                "text": "有新的訪客，請直接回應要開啟門鎖的秒數；若不願意開啟門鎖，可忽略或回復 0 。"},
            {
                "type": "image",
                "originalContentUrl": "https://khaos.tw/show/guest_photo.jpg",
                "previewImageUrl": "https://khaos.tw/show/guest_photo_.jpg"
            }]
    }
    response = requests.post('https://api.line.me/v2/bot/message/broadcast',
                             data=json.dumps(lineData), headers=lineHeader)

    return jsonify({"success": 0, "msg": "upload successful!", "line_bot": response.text})

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

# LINE BOT 控制開關門鎖
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # line_bot_api.reply_message(
    # event.reply_token,
    # TextSendMessage(text=event.message.text))
    msg = event.message.text
    try:
        t = int(msg)
        if(t < 0 or t > 120):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="開門的時間需介於 0 ~ 120 秒"))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="門鎖已解除 " + msg + " 秒"))
            open_door(t)
    except ValueError:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入數值..."))

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
