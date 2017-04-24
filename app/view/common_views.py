from flask import Blueprint
import json
from flask import Flask
from flask import request,render_template
from flask import redirect
from flask import jsonify
from app.utils import send_message
from app.model.DBUtil import *
vcommon=Blueprint('vcommon',__name__)
@vcommon.route('/register' )
def register():
    if request.method == 'POST':
        a = request.get_data()
        dict = json.loads(a)
        isexcited,exp=DBUtil.check_user_mail_duplicated(dict['mail'])
        isexcited2,exp=DBUtil.check_user_name_duplicated(dict['name'])
        if(isexcited or isexcited2):
            dict2 = {'status': '0', 'userid': -1, 'errcode': 'duplicated'};
            return json.dumps(dict2)
        uid, exp = DBUtil.insert_new_user(dict)
        ret=send_message.mail(userid=dict['name'], receiver=dict['mail'])
        if not ret:
            print("the email might not be right")
            dict2 = {'status': '0', 'userid': -1, 'errcode': 'wrong email'};

        if uid is not 0:
            print("user is created, id is '%d'" % uid)
            dict2 = {'status': '1', 'userid': uid,'errcode':'null'};
        else:
            dict2 = {'status': '0', 'userid': -1,'errcode':exp};
        return json.dumps(dict2)
    else:
        return '400'


@vcommon.route('/login')
def login():
    return("successful")

@vcommon.route('/activate/<token>')
def activate(token):
     email = send_message.confirm_token(token)
     #need to change the database due to the emailaddress
     return(email)


from app.utils import send_message
@vcommon.route('/testmail')
def testmail():
    ret=send_message.mail(1001,'1271369334@qq.com')
    return ('true')






