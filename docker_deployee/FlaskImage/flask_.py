from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response
import time
import os
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route('/test')
def test():
    return "test5 ~"

@app.route('/')
def index():
    return render_template('index.html')

#初始化資料庫
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
    if entry is None: # 'No entry found'
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
                VALUE = 'no' where KEY = 'Locked'") # 門是開的
    conn.commit()
    conn.close()

    time.sleep(t)

    conn = sqlite3.connect('iot.db')
    c = conn.cursor()
    c.execute("UPDATE STATUS SET \
                VALUE = 'yes' where KEY = 'Locked'") #門是關的
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
    if(result=='yes'):
        return jsonify(True) # 門是關的
    else:
        return jsonify(False) # 門是開的

# 根據給定的時間 判斷是否有新的訪客過來
@app.route('/has_guest_since/<int:lgct>', methods=['GET'])
def has_guest_since(lgct):
    mtime = int(os.path.getmtime('./upload/guest_photo.jpg')) #檔案上次修改的時間
    if(lgct < mtime):
        return jsonify(True)
    else:
        return jsonify(False)

# 上傳使用者的新相片
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
