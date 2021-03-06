from flask import Blueprint
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from datetime import  datetime
from datetime import  timedelta
from app.model.models import TGroup,TActivity
import json
from app.model.DBUtil import *
vgroup=Blueprint('vgroup',__name__)
@vgroup.route('/get_activity_list/<group_id>',methods=['POST'])
def getActList(group_id):
    list=DBUtil.retrieve_activitiy_by_group(group_id, datetime.now() - timedelta(days=200), 999)
    ##deal with the list
    list2=[]
    for act in list:
        list2.append(act.id)
    return json.dumps({'status': 1, 'activity_list': list2, 'exp': 'none'})
    pass

@vgroup.route('/get_focused_group_list/<user_id>',methods=['POST'])
def get_focused(user_id):
    group_list=DBUtil.retrieve_user_groups(user_id)
    list=[]
    for g in group_list:
        list.append(g.id)
    dict = {'status': 1, 'group_list': list, 'exp': 'none'};
    return json.dumps(dict)

@vgroup.route('/admit_focus_group/<user_id>',methods=['POST'])
def focusGroup(user_id):
    a = request.get_data()
    dict = json.loads(a)
    list=[dict['group_id']]
    status=DBUtil.add_user_group(user_id,list)
    dict2 = {'status': status, 'group_id': dict['group_id'], 'exp': 'none'};
    return json.dumps(dict2)



@vgroup.route('/cancel_focus_group/<user_id>',methods=['POST'])
def cancelFocused(user_id):
    a = request.get_data()
    dict = json.loads(a)
    status = DBUtil.unfollow_group(user_id, dict['group_id'])
    dict2 = {'status': status, 'group_id': dict['group_id'], 'exp': 'none'};
    return json.dumps(dict2)


@vgroup.route('/getgroup/<group_id>',methods=['POST'])
def getgroup(group_id):
    group = DBUtil.retrieve_group_by_id(group_id)
    group_dict={}
    group_dict['name'] = group.name
    group_dict['id'] = group.id
    group_dict['description'] = group.description
    group_dict['focus_count']=group.attention_count
    group_dict['act_count']=group.activetity_count
    group_dict['status']=1
    group_dict['exp']='none'
    return json.dumps(group_dict)


