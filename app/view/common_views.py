from flask import Blueprint
import json
from flask import Flask
from flask import request,render_template
from flask import redirect
from flask import jsonify
from app.utils import send_message
from app.model.DBUtil import *
vcommon=Blueprint('vcommon',__name__)
@vcommon.route('/register',methods=['POST'] )
def register():
    if request.method == 'POST':
        a = request.get_data()
        dict = json.loads(a)
        dict['avatar']=4
        isexcited,exp=DBUtil.check_user_mail_duplicated(dict['mail'])
        isexcited2,exp=DBUtil.check_user_name_duplicated(dict['name'])
        isexcited3,exp=DBUtil.check_user_phone_duplicated(dict['phone'])
        if(isexcited or isexcited2 or isexcited3):
            dict2 = {'status': '0', 'userid': -1, 'errcode': 'duplicated'};
            return json.dumps(dict2)
        dict["is_activated"] = 'n'
        dict["avatar"]="-1"
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
'''注册用路由 接受json格式如下测试'''

@vcommon.route('/login',methods=['POST'])
def login():
    a = request.get_data()
    dict = json.loads(a)
    ismatched, exp = DBUtil.check_user_mail_and_psw(dict['name'],dict['password'])
    if ismatched:
        user_id=DBUtil.retrieve_userid_by_mail(dict['name'])
        dict2={'status':1,'userid':user_id,'errorcode':exp}
        ##login_manager.login_user(user_id)
    else:
        dict2 = {'status': 0, 'userid': -1, 'errorcode': exp}
    return json.dumps(dict2)

@vcommon.route('/activate/<token>')
def activate(token):
     email = send_message.confirm_token(token)
     state,exp=DBUtil.update_user_mail_state(email, True)
     if state:
      return(email+' activated')
     else: return('false '+exp)


from app.utils import send_message
@vcommon.route('/testmail')
def testmail():
    ret=send_message.mail(1001,"13717680252@163.com")
    return ('true')


@vcommon.route('/test')
def testdb():
    isexcited, exp = DBUtil.check_user_mail_duplicated('123.qq.com')
    print(isexcited)
    new_user = {"name": 'wangtianran', "password": '123456', "mail": '1271369334@qq.com',
                "phone": '1008600', "stu_id": '14301020', "college": '北交大',
                "profession": 'xxx', "sex": 'm', "birthdate": "1996-01-01", "is_activated": 'n'}
    uid, exp = DBUtil.insert_new_user(new_user)
    print(exp)
    return('testing page')

