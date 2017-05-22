from flask import Blueprint
import json
from flask import Flask
from flask import request, render_template
from flask import redirect
from flask import jsonify
from app.utils import send_message
from app.model.DBUtil import *
from datetime import datetime
from app.utils.comment_servive import *
vservice = Blueprint('vservice', __name__)
r = redis.Redis(host='localhost', port=6379,db=4)
@vservice.route('/invitation/<user_id>',methods=['POST'])
def invatation_service(user_id):
    friend_id=r.lpop("invitation:" + user_id)
    text=r.lpop("invitation:" + user_id)
    dict={}
    if friend_id is None:
        dict['status'] = '0';

    else:
        dict['friend_id'] = str(friend_id, "utf-8")
        dict['text'] = str(text, "utf-8")
        dict['status']='1'
    return json.dumps(dict)

@vservice.route('/changedescription/<user_id>',methods=['POST'])
def change_description(user_id):
    activity_id=r.lpop("changing:" + user_id)
    text=r.lpop("changing:" + user_id)
    time=r.lpop("changing:" + user_id)
    dict={}
    if activity_id is None:
        dict['status'] = 0
    else:
        dict['status'] = '1'
        dict['activity_id'] = str(activity_id,"utf-8")
        dict['text'] = str(text,"utf-8")
        dict['time'] = str(time,"utf-8")
    return json.dumps(dict)


@vservice.route('/comingactivity/<user_id>',methods=['POST'])
def comingactivity(user_id):
    list = DBUtil.retrieve_user_activities(user_id)
    now = datetime.now()
    for act in list:
        time= datetime.datetime.strftime(act.start_date, '%Y-%m-%d %H:%M:%S')
        now.strftime('%Y-%m-%d %H:%M:%S')
    return("successful")

@vservice.route('/notest')
def notest():
    friend_id=r.lpop("invitation:22" )
    text=r.lpop("invitation:22")
    if friend_id is None:
     return('none')
    return(friend_id)

