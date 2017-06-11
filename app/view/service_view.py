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
    length=r.llen("invitation:" + user_id)
    dict = {}
    idlist=[]
    textlist=[]
    for i in length:
     friend_id=str(r.lpop("invitation:" + user_id),"utf-8")
     text=str(r.lpop("invitation:" + user_id),"utf-8")
     if(friend_id not in idlist):
         idlist.append(friend_id)
         textlist.append(text)
    dict["id"]=idlist
    dict["text"]=textlist
    dict['numbers'] = len(idlist)
    dict['status']='1'
    return json.dumps(dict)


@vservice.route('/invitation_num/<user_id>')
def invatation_nums(user_id):
    dict={}
    length=r.llen("invitation:" + user_id)
    dict['numbers'] =length
    print(dict['numbers'] )
    dict['status']='1'
    return ("yes")


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
        timenow=now.strftime('%Y-%m-%d %H:%M:%S')

    return("successful")


@vservice.route('/notest')
def notest():
    friend_id=r.lpop("invitation:22" )
    text=r.lpop("invitation:22")
    if friend_id is None:
     return('none')
    return(friend_id)


