from flask import Blueprint
import json
from flask import Flask
from flask import request, render_template
from flask import redirect
from flask import jsonify
from app.utils import send_message
from app.model.DBUtil import *
from app.utils.comment_servive import *
vcomment = Blueprint('vcomment', __name__)


@vcomment.route('/activity_comment',methods=['POST'] )
def commit_comment():
    if request.method == 'POST':
        c_request = request.get_data()
        dict = json.loads(c_request)
        commentid, exp = DBUtil.insert_new_comment_activity(dict)
        if commentid is not 0:
            print("comment is created, id is '%d'" % commentid)
            dict2 = {'status': '1', 'commentid': commentid, 'errcode': 'null'};
            activity_comment(dict)
        else:
            dict2 = {'status': '0', 'commentid': -1, 'errcode':exp};
        return json.dumps(dict2)

    else:
        return '400'


@vcomment.route('/comment_person',methods=['POST'] )
def commit_comment_person():
    if request.method == 'POST':
        c_request = request.get_data()
        dict = json.loads(c_request)
        commentid, exp = DBUtil.insert_new_comment_person(dict)
        if commentid is not 0:
            print("comment is created, id is id'%d'" % commentid)
            dict2 = {'status': '1', 'commentid': commentid, 'errcode': 'null'}
            user_comment(dict)
        else:
            dict2 = {'status': '0', 'comment': -1, 'errcode': exp};
        return json.dumps(dict2)
    else :
      return '400'

@vcomment.route("/test_comment")
def testcomment():
        dict={}
        dict['act_id']=7
        dict["comm_user_id"]=22
        dict["commed_user_id"]=23
        dict['level']=3
        dict['content']="dwadadada"
        commentid, exp = DBUtil.insert_new_comment_person(dict)
        if commentid is not 0:
            print("comment is created, id is id'%d'" % commentid)
            user_comment(dict)
        return"233"

