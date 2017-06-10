from flask import Blueprint
from app.model.DBUtil import *
from flask import Blueprint
import json
from flask import Flask
from flask import request, render_template
from flask import redirect
from flask import jsonify
vfriend=Blueprint('vfriend',__name__)
r = redis.Redis(host='localhost', port=6379,db=4)

@vfriend.route('/get_friend_list/<user_id>',methods=['POST'])
def getFriendList(user_id):
    if request.method == 'POST':

        friendlist, exp = DBUtil.retrieve_user_friendslist(user_id=user_id)
        friendlist=friendlist.strip()
        list=friendlist.split(",")
        dict2 = {'status': '1', 'friendlist': list, 'errcode': exp};
        return json.dumps(dict2)
    else:
        return '400'

@vfriend.route('/send_text',methods=['POST'])
def sendText():
    return('succeed2')

@vfriend.route('/send_friend_invitation')
def invitation():
    dict2 = {'status': '1', 'errcode': "none"};
    if request.method == 'POST':
        a = request.get_data()
        dict = json.loads(a)
        userid = dict['userid']
        friendid = dict['friendid']
        text = dict['text']
        r.lpush("invitation:" + friendid, text)
        r.lpush("invitation:"+friendid, userid)
    return json.dumps(dict2)


@vfriend.route('/reply_invitation')
def reply_invitation():
    if request.method == 'POST':
        a = request.get_data()
        dict = json.loads(a)
        invitor=dict['invitor']
        receiver=[dict['receiver']]
        DBUtil.update_user_friends(receiver, [str(invitor)])
        status, exp = DBUtil.update_user_friends(invitor,[str(receiver)])
        if  status=='ok':
            print("ok!" )
            dict2 = { 'status': status, 'userid':invitor,'errcode': 'null'};
        else:
            dict2 = {'status': status, 'userid': -1, 'errcode':exp};
        return json.dumps(dict2)
    else:
        return '400'

@vfriend.route('/testfriend')
def test():
        # userid = '1'
        # friendid = '22'
        # text = "caonima"
        # r.lpush("invitation:"+friendid, text)
        # r.lpush("invitation:"+friendid, friendid)
        # r.lpush("changing:22", "1995-09-09")
        # r.lpush("changing:22" ,"description")
        # r.lpush("changing:22", "1")
        DBUtil.update_user_friends(22, ['24'])
        DBUtil.update_user_friends(24, ['22'])
        DBUtil.update_user_friends(22, ['23'])
        DBUtil.update_user_friends(23, ['22'])
        return ("successful")