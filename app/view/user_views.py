from flask import Blueprint
import json
import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from app.model.DBUtil import *
from app.model.models import TActivity
from app.model.DBUtil import *
from app.utils.search_server import*
vuser=Blueprint('vuser',__name__)
@vuser.route('/get_user_info/<user_id>',methods=['POST'])
def getUserInof(user_id):
    dict={}
    dict=DBUtil.retrieve_userinfo_by_id(user_id)
    print(dict)
    if dict==None:

        dict['status'] = "0"
    else :
        dict['date'] = dict['birthdate'].strftime('%Y-%m-%d')
        dict["birthdate"] = ""
        dict['status']='1'
    return (json.dumps(dict))


@vuser.route('/get_credit_list/<user_id>')
def getCreditList(user_id):
    pass


@vuser.route('/change_my_info/<user_id>',methods=['POST'])
def changeInfo(user_id):
    c_request = request.get_data()
    dict = json.loads(c_request)
    state, exp=DBUtil.update_userinfo(user_id,dict)
    dict2 = {'status': '1', 'state': state, 'errcode': exp};
    return json.dumps(dict2)

@vuser.route('/search_user/<key>',methods=['POST'])
def searchuser(key):
    list=searchfriend(key)
    dict2 = {'status': '1', 'result': list, 'errcode': "none"};
    return json.dumps(dict2)

@vuser.route("/change_user_avatar")
def change_avatar():
    c_request = request.get_data()
    dict = json.loads(c_request)
    status=DBUtil.update_user_avatar(dict["user_id"],dict["pic_id"])
    dict2={status:"1","TOF":status}
    return json.dumps(dict2)


