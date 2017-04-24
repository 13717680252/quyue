from flask import Blueprint
import json
from flask import Flask
from flask import request, render_template
from flask import redirect
from flask import jsonify
from app.utils import send_message
from app.model.DBUtil import *

vcomment = Blueprint('vcommon', __name__)


@vcomment.route('/commit_comment')
def commit_comment():
    if request.method == 'POST':
        c_request = request.get_data()
        dict = json.loads(c_request)
        commentid, exp = DBUtil.insert_new_comment_activity(dict)
        if commentid is not 0:
            print("comment is created, id is '%d'" % commentid)
            dict2 = {'status': '1', 'commentid': commentid, 'errcode': 'null'};
        else:
            dict2 = {'status': '0', 'commentid': -1, 'errcode':exp};
        return json.dumps(dict2)
    else:
        return '400'


@vcomment.route('/commit_person_comment')
def commit_comment_person():
    if request.method == 'POST':
        c_request = request.get_data()
        dict = json.loads(c_request)
        commentid, exp = DBUtil.insert_new_comment_person(dict)
        if commentid is not 0:
            print("comment is created, id is id'%d'" % commentid)
            dict2 = {'status': '1', 'commentid': commentid, 'errcode': 'null'};
        else:
            dict2 = {'status': '0', 'comment': -1, 'errcode': exp};
        return json.dumps(dict2)
    else :
     return '400'
