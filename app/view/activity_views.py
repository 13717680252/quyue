from flask import Blueprint
import json
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from app.model.DBUtil import *
from app.model.models import TActivity
vactivity=Blueprint('vactivity',__name__)

@vactivity.route('/get_activity_details/<activity_id>',methon=['POST'])
def getActDetails(activity_id):
    act=DBUtil.retrieve_activity_by_id(activity_id)
    act_dict={}
    act_dict['id']=act.id
    act_dict['publisher']=act.publisher
    act_dict['group_id']=act.group_id
    act_dict['description']=act.discption
    act_dict['create_date']=act.create_date
    act_dict['start_date']=act.start_date
    act_dict['end_date']=act.end_date
    act_dict['min_num']=act.min_num
    act_dict['max_num']=act.max_num
    act_dict['cur_num']=act.cur_num
    act_dict['join_ids']=act.join_ids
    act_dict['is_expired']=act.is_expired
    act_dict['tags']=act.tags
    act_dict['is_canceled']=act.is_canceled
    act_dict['cancel_date']=act.cancel_date
    act_dict['status']=1
    act_dict['exp']='none'
    return json.dumps[act_dict]
@vactivity.route('/get_user_activity_list/<user_id>',methon=['POST'])
def getUserActList(user_id):
    list=[]
    exp='none'
    list2=[]
    try:
     list=DBUtil.retrieve_user_activities(user_id)
     for act in list:
         list2.append[act.id]
    except:
        exp='failed'
    dict = {'status': '1', 'activity': list2,'exp':exp};
    return json.dumps(dict)
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

##加入活动
@vactivity.route('/join_activity/',methods=['POST'])
def join():
    a = request.get_data()
    dict = json.loads(a)
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
     dict2= dict2 = {'status': 1, 'activity_id': -1, 'exp': exp};
    return json.dumps(dict2)

@vactivity.route('/get_member_list/<activity_id>')
def getMemberList(activity_id):
    pass

