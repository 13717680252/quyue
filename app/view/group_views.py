from flask import Blueprint
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from datetime import  datetime
from datetime import  timedelta
import json
from app.model.DBUtil import *
vgroup=Blueprint('vgroup',__name__)
@vgroup.route('/get_activity_list/<group_id>')
def getActList(group_id):
    list=DBUtil.retrieve_activitiy_by_group(group_id, datetime.now() - timedelta(days=200), 999)
    ##deal with the list
    return json.dumps({'status': 1, 'activity_list': list, 'exp': 'none'})
    pass

@vgroup.route('/get_focused_group_list/<user_id>',method=['POST'])
def get_focused(user_id):
    group_list=DBUtil.retrieve_user_groups(user_id)
    dict = {'status': 1, 'group_list': group_list, 'exp': 'none'};
    return json.dumps(dict)

@vgroup.route('/admit_focus_group/<user_id>',method=['POST'])
def focusGroup(user_id):
    a = request.get_data()
    dict = json.loads(a)
    list=[dict['group_id']]
    status=DBUtil.add_user_group(user_id,list)
    dict2 = {'status': status, 'group_id': dict['group_id'], 'exp': 'none'};
    return json.dumps(dict2)
    pass

@vgroup.route('/cancel_focus_group/<user_id>')
def cancelFocused(user_id):
    pass

#
@vgroup.route('/addgroup')
def addgroup():
    pass

