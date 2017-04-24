from flask import Blueprint
from app.model.DBUtil import *
from flask import Blueprint
import json
from flask import Flask
from flask import request, render_template
from flask import redirect
from flask import jsonify
vfriend=Blueprint('vfriend',__name__)

@vfriend.route('/get_friend_list/<user_id>')
def getFriendList(user_id):
    pass

@vfriend.route('/send_text')
def sendText():
    return('succeed2')

@vfriend.route('/send_friend_invitation')
def invitation():
    pass

@vfriend.route('/reply_invitation')
def reply_invitation():
    if request.method == 'POST':
        a = request.get_data()
        dict = json.loads(a)
        invitor=dict['invitor']
        receiver=[dict['receiver']]
        status, exp = DBUtil.update_user_friend(invitor,receiver)
        if  status=='ok':
            print("ok!" )
            dict2 = { 'status': status, 'errcode': 'null'};
        else:
            dict2 = {'status': status, 'userid': -1, 'errcode':exp};
        return json.dumps(dict2)
    else:
        return '400'
