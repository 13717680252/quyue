from flask import Blueprint
import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from app.model.DBUtil import *
vactivity=Blueprint('vactivity',__name__)
@vactivity.route('/get_activity_list/<group_id>')
def getActList(group_id):
    pass

@vactivity.route('/get_activity_details/<activity_id>')
def getActDetails(activity_id):
    pass

@vactivity.route('/get_user_activity_list/<user_id>')
def getUserActList(user_id):
    pass

@vactivity.route('/get_past_activity_list/<user_id>')
def getPastActList(user_id):
    pass

@vactivity.route('/admit_activity/',methods=['POST'] )
def admitAct():
    if request.method == 'POST':
        c_request = request.get_data()
        dict = json.loads(c_request)
        actid, exp = DBUtil.insert_new_activity(dict)
        if actid is not 0:
            print("user is created, id is '%d'" % actid)
            dict2 = {'status': '1', 'actid':actid, 'errcode': 'null'};
        else:
            dict2 = {'status': '0', 'actid': -1, 'errcode': exp};
        return json.dumps(dict2)
    else:
        return '400'

@vactivity.route('/get_member_list/<activity_id>')
def getMemberList(activity_id):
    pass

