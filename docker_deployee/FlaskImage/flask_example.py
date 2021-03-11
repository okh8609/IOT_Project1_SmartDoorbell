import json
import requests
import threading


from flask import Flask, request, abort


import http

#from uwsgi import *
from datetime import datetime
from threading import Timer
from threading import Thread

#from sympy import false

app = Flask(__name__)

IncomingCall = '0'
IncomingCall_ID = 0
Person = ''
Meeting_title = 'rrr'

Mess_URL = 'https://webexapis.com/v1/messages'
Meet_URL = 'https://webexapis.com/v1/meetings'




Get_Mess_Params = {
        'roomId': 'Y2lzY29zcGFyazovL3VzL1JPT00vNjJiODZjZjAtY2MzOC0xMWVhLWE2MjQtZGI1YzM0N2FhMzNl',
        'max': '1'
}


Post_Meet_Params = {
        'title': str(Meeting_title),
        'password': "0000",
        'start': datetime.now().replace(microsecond=0).isoformat()+"-00:00",
        'end': datetime.now().replace(microsecond=0).isoformat()+"-01:00"
      #  'enabledAutoRecordMeeting': datetime.now().replace(microsecond=0).isoformat()+"-07:00",
       # 'allowAnyUserToBeCoHost': 'false'
}

expires_in = 10 #更新的週期(secs)
refreshing = False

def refreshToken():
    refreshing = True

    f = open("tokens.txt", "r")
    preData = json.loads(f.read())
    
    baseURL = 'https://webexapis.com/v1/access_token'
    myHeader = {
        'Content-type': 'application/json'
    }
    myData = {
        'grant_type' : "refresh_token",
        'client_id' : "C046b07944e254c258194e0412a27db01cd0bebea39367b8ad340db19348a8333",
        'client_secret' : "e3dc1a03856c73283cf0738e06c2686bf8b5c717b58a8893cbc05865cc4d9ef1",
        'refresh_token' : preData['refresh_token']
    }
    response = requests.post(baseURL, data=json.dumps(myData), headers=myHeader)
    print(">> def refreshToken():")
    print(json.dumps( json.loads(response.text) , indent=2))
    #儲存
    f = open("tokens.txt", "w")
    f.write(response.text)
    f.close()
    #更新expires_in
    data = json.loads(response.text)
    expires_in = data["expires_in"] - 3600 # 提早一個小時更新Token
    threading.Timer(expires_in, refreshToken).start()

@app.route('/oauth2', methods=['GET'])
def getNewAccessToken():
    ''' 取得 oauth2 的 auth code
    https://webexapis.com/v1/authorize?client_id=C046b07944e254c258194e0412a27db01cd0bebea39367b8ad340db19348a8333&response_type=code&redirect_uri=http%3A%2F%2Fkaihao.top%2Foauth2&scope=spark-compliance%3Amemberships_read%20spark-admin%3Aresource_groups_read%20meeting%3Arecordings_read%20spark%3Aall%20meeting%3Apreferences_write%20spark-admin%3Apeople_write%20spark-admin%3Aorganizations_read%20spark-admin%3Aplaces_read%20spark-compliance%3Ateam_memberships_read%20meeting%3Aschedules_write%20spark-compliance%3Ateam_memberships_write%20spark-admin%3Adevices_read%20spark-admin%3Ahybrid_clusters_read%20spark-compliance%3Amessages_read%20spark-admin%3Adevices_write%20meeting%3Aschedules_read%20spark-compliance%3Amemberships_write%20identity%3Aplaceonetimepassword_create%20spark-admin%3Aroles_read%20meeting%3Arecordings_write%20meeting%3Apreferences_read%20spark-admin%3Aresource_group_memberships_read%20spark-compliance%3Aevents_read%20spark-admin%3Aresource_group_memberships_write%20spark-compliance%3Arooms_read%20spark-admin%3Acall_qualities_read%20spark-compliance%3Amessages_write%20spark%3Akms%20spark-admin%3Ahybrid_connectors_read%20audit%3Aevents_read%20spark-compliance%3Ateams_read%20spark-admin%3Aplaces_write%20spark-admin%3Alicenses_read%20spark-admin%3Apeople_read&state=set_state_here
    '''
    authCode = request.args.get('code')
    print(authCode)

    #取得 Access Token
    baseURL = 'https://webexapis.com/v1/access_token'
    myHeader = {
        'Content-type': 'application/json'
    }
    myData = {
        'grant_type' : "authorization_code",
        'client_id' : "C046b07944e254c258194e0412a27db01cd0bebea39367b8ad340db19348a8333",
        'client_secret' : "e3dc1a03856c73283cf0738e06c2686bf8b5c717b58a8893cbc05865cc4d9ef1",
        'code' : authCode,
        'redirect_uri' : "https://bobii.kaihao.top/oauth2"
    }

    response = requests.post(baseURL, data=json.dumps(myData), headers=myHeader)
    print(">> def getNewAccessToken():")
    print(json.dumps( json.loads(response.text) , indent=2))

    f = open("tokens.txt", "w")
    f.write(response.text)
    f.close()

    #更新expires_in
    data = json.loads(response.text)
    try:
        expires_in = data["expires_in"] - 3600 # 提早一個小時更新Token
        if (refreshing == False):
            threading.Timer(expires_in, refreshToken).start()
    except KeyError:
        print('["expires_in"] not exist')


    msg = "HTTP status_code of Webex API = " + str(response.status_code)
    if (response.status_code != 200):
        msg += "</br></br>Something Wrong! -> Please goto: </br></br>https://webexapis.com/v1/authorize?client_id=C046b07944e254c258194e0412a27db01cd0bebea39367b8ad340db19348a8333&response_type=code&redirect_uri=http%3A%2F%2Fkaihao.top%2Foauth2&scope=spark-compliance%3Amemberships_read%20spark-admin%3Aresource_groups_read%20meeting%3Arecordings_read%20spark%3Aall%20meeting%3Apreferences_write%20spark-admin%3Apeople_write%20spark-admin%3Aorganizations_read%20spark-admin%3Aplaces_read%20spark-compliance%3Ateam_memberships_read%20meeting%3Aschedules_write%20spark-compliance%3Ateam_memberships_write%20spark-admin%3Adevices_read%20spark-admin%3Ahybrid_clusters_read%20spark-compliance%3Amessages_read%20spark-admin%3Adevices_write%20meeting%3Aschedules_read%20spark-compliance%3Amemberships_write%20identity%3Aplaceonetimepassword_create%20spark-admin%3Aroles_read%20meeting%3Arecordings_write%20meeting%3Apreferences_read%20spark-admin%3Aresource_group_memberships_read%20spark-compliance%3Aevents_read%20spark-admin%3Aresource_group_memberships_write%20spark-compliance%3Arooms_read%20spark-admin%3Acall_qualities_read%20spark-compliance%3Amessages_write%20spark%3Akms%20spark-admin%3Ahybrid_connectors_read%20audit%3Aevents_read%20spark-compliance%3Ateams_read%20spark-admin%3Aplaces_write%20spark-admin%3Alicenses_read%20spark-admin%3Apeople_read&state=set_state_here"
 
    return msg


@app.route('/accToken_debug', methods=['GET'])
def getAccessToken():
    f = open("tokens.txt", "r")
    data = json.loads(f.read())
    return data["access_token"]


def rst_IncomingCall():
    global IncomingCall
    IncomingCall = '0'
    print("Reset Incoming call")
  #  Timer(20, rst_IncomingCall).start()


#@rbtimer(5)
#def five_seconds(num):
 #   return

@app.route('/webhook', methods=['POST'])
def POST_from_Webex():

    myHeader = {
            'Authorization': ('Bearer ' + getAccessToken()).encode('utf-8'),
            'Content-type': 'application/json'
    }

    global IncomingCall
    global IncomingCall_ID
    global Person
    #get newest text
    response = requests.get(Mess_URL, params=Get_Mess_Params, headers=myHeader)
    response_dict= json.loads(response.text)
    messenge = json.dumps(response_dict, indent=2)
    messenge = messenge.replace('[', '')
    messenge = messenge.replace(']', '')
    #print(messenge)
   # eval(messenge)
    message_dict = eval(messenge)
    mess_context= message_dict['items']['text']
    print(message_dict['items']['text'])
    default_str = '準備開會囉！'
    if mess_context == default_str:
        IncomingCall_ID = IncomingCall_ID+1
        IncomingCall = str(IncomingCall_ID)
        Person = message_dict['items']['text']
        requests.post(Meet_URL, params=Post_Meet_Params, headers=myHeader)
        t = Timer(60.0, rst_IncomingCall)
        t.start()
      #  print(json.dumps(json.loads(response.text), indent=2))
    return '8888'


#APP得到 是否有來電
@app.route('/IncomingCall', methods=['GET'])
def Get_from_app():
    global IncomingCall
    return IncomingCall

#得到 會議密碼及


@app.route('/home')
def homepage():
    return 'Hello, World!!!'

@app.route('/test')
def in_test_page():
    return 'In test page'

if __name__ == "__main__":
    #app.run()
    app.run(debug=True, host='0.0.0.0', port=8888)



