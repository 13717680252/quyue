from flask import Blueprint
import json
from datetime import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from app.model.DBUtil import *
from app.model.models import TActivity
from app.utils import search_server
vactivity=Blueprint('vactivity',__name__)

@vactivity.route('/get_activity_details/<activity_id>',methods=['POST'])
def getActDetails(activity_id):
    act=DBUtil.retrieve_activity_by_id(activity_id)
    act_dict={}
    act_dict['id']=act.id
    act_dict['publisher']=act.publisher
    act_dict['group_id']=act.group_id
    act_dict['description']=act.description
    act_dict['create_date']= datetime.datetime.strftime(act.create_date, '%Y-%m-%d %H:%M:%S')
    act_dict['start_date']=datetime.datetime.strftime(act.start_date, '%Y-%m-%d %H:%M:%S')
    act_dict['end_date']=datetime.datetime.strftime(act.end_date, '%Y-%m-%d %H:%M:%S')
    act_dict['min_num']=act.min_num
    act_dict['max_num']=act.max_num
    act_dict['cur_num']=act.cur_num
    act_dict['join_ids']=act.join_ids
    act_dict['is_expired']=act.is_expired
    act_dict['tags']=act.tags
    act_dict['is_canceled']=act.is_canceled
    if act.is_canceled==0:
        act_dict['cancel_date']=("2999-12-30 24:60:60")
    else:
        act_dict['cancel_date']=datetime.datetime.strftime(act.cancel_date, '%Y-%m-%d %H:%M:%S')
    act_dict['status']=1
    act_dict['exp']='none'
    return json.dumps(act_dict)

@vactivity.route('/get_user_activity_list/<user_id>',methods=['POST'])
def getUserActList(user_id):
    list=[]
    exp='none'
    list2=[]
    try:
     list=DBUtil.retrieve_user_activities(user_id)
     for act in list:
         if act.is_canceled==0:
          list2.append[act.id]
    except:
        exp='failed'
    dict = {'status': '1', 'activity': list2,'exp':exp};
    return json.dumps(dict)
    pass


@vactivity.route('/get_past_activity_list/<user_id>')
def getPastActList(user_id):
    list = []
    exp = 'none'
    list2 = []
    try:
        now = datetime.now()
        list = DBUtil.retrieve_user_activities(user_id)
        for act in list:
            if act.is_canceled == 0 and act.end_date:
                list2.append[act.id]
    except:
        exp = 'failed'
    dict = {'status': '1', 'activity': list2, 'exp': exp};
    return json.dumps(dict)
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
            list=[]
            list.append[actid]
            DBUtil.join_activity(dict['publisher'], list)
        else:
            dict2 = {'status': '0', 'actid': -1, 'errcode': exp};
        return json.dumps(dict2)
    else:
        return '400'

##加入活动
@vactivity.route('/join_activity/',methods=['POST'])
def join():
    a = request.get_data()
    dict = json.loads(a)
    list=[]
    list = [dict['activity_id']]
    user_id=dict['user_id']
    exp='none'
    try:
     DBUtil.join_activity(user_id, list)
    except:
     exp='failed'
    dict2 = {'status': 1, 'activity_id': dict['activity_id'], 'exp':exp};
    return json.dumps(dict2)

@vactivity.route('/quit_activity',methods=['POST'])
def quit():
    dict=json.loads(request.get_data())
    list=[dict['activity_id']]
    user_id=dict['user_id']
    exp='none'
    d_list=[]
    try:
        d_list=DBUtil.remove_user_activities(user_id,list)
    except:
        exp='failed'
    if len(d_list)>0:
     dict2 = {'status': 1, 'activity_id':d_list[0] , 'exp':exp};
    else:
     dict2 = {'status': 1, 'activity_id': -1, 'exp': exp};
    return json.dumps(dict2)

@vactivity.route('/searchact',methods=['POST'])
def searchact():
    dict=json.loads(request.get_data())
    g_id=dict['groupid']
    list=dict['lables']
    key=dict['key']
    ret=search_server.searchactivity(g_id,list,key)
    dict = {'status': 1, 'activity_id': ret, 'exp': 'none'}
    return json.dumps(dict)



@vactivity.route('/get_member_list/<activity_id>')
def getMemberList(activity_id):
    list=DBUtil.retrieve_joined_people_of_activity(activity_id)
    if list!=None:
      dict2 = {'status': 1, 'activity_id': list, 'exp':"none"};
    else :
        dict2={'status': 0,'exp':"none member"}
    return json.dumps(dict2)

@vactivity.route("/insertactivity")
def insertactivity():
    s = datetime.now()
    e = datetime.now()
    activity = {"name": '新活动3', "publisher": 22, "group_id": 2, "description": 'a description',
                "start_date": s, "end_date": e, "min_num": 2, "max_num": 10, "cur_num": 3,
                "join_ids": '', "tags": '聚餐,交友', "is_canceled": 0}
    states,exp=DBUtil.insert_new_activity(activity)

    return str(states)

@vactivity.route("/testjoin")
def testjoin():
    d_list = DBUtil.remove_user_activities(22, ['2'])
    list=DBUtil.retrieve_user_activities(22)
    ids=[]
    for i in list:
        ids.append(i.id)
    return str(ids)

