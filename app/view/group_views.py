from flask import Blueprint
from app.model.DBUtil import *
vgroup=Blueprint('vgroup',__name__)
@vgroup.route('/get_activity_list/<group_id>')
def getActList(group_id):
    pass

@vgroup.route('/get_focused_group_list/<user_id>')
def get_focused(user_id):
    pass

@vgroup.route('/admit_focus_group/<user_id>')
def focusGroup(user_id):
    pass

@vgroup.route('/cancel_focus_group/<user_id>')
def cancelFocused(user_id):
    pass

#
@vgroup.route('/addgroup')
def addgroup():
    pass

