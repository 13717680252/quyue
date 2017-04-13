import json
from flask import Blueprint

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

@vactivity.route('/admit_activity/')
def admitAct():
    pass

@vactivity.route('/get_member_list/<activity_id>')
def getMemberList(activity_id):
    pass

