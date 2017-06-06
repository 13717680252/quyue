from flask import Blueprint
import json
import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from app.model.DBUtil import *
from app.model.models import TActivity
from app.model.DBUtil import *
from app.utils.search_server import*
from app.utils.test import*
vuser=Blueprint('vuser',__name__)
@vuser.route('/get_user_info/<user_id>',methods=['POST'])
def getUserInof(user_id):
    dict={}
    dict=DBUtil.retrieve_userinfo_by_id(user_id)
    print(dict)
    if dict==None:

        dict['status'] = "0"
    else :
        dict['date'] = dict['birthdate'].strftime('%Y-%m-%d')
        dict["birthdate"] = ""
        dict['status']='1'
    return (json.dumps(dict))


@vuser.route('/get_credit_list/<user_id>')
def getCreditList(user_id):
    pass


@vuser.route('/change_my_info/<user_id>',methods=['POST'])
def changeInfo(user_id):
    c_request = request.get_data()
    dict = json.loads(c_request)
    state, exp=DBUtil.update_userinfo(user_id,dict)
    dict2 = {'status': '1', 'state': state, 'errcode': exp};
    return json.dumps(dict2)

@vuser.route('/search_user/<key>',methods=['POST'])
def searchuser(key):
    list=searchfriend(key)
    dict2 = {'status': '1', 'result': list, 'errcode': "none"};
    return json.dumps(dict2)

@vuser.route("/change_user_avatar")
def change_avatar():
    c_request = request.get_data()
    dict = json.loads(c_request)
    status=DBUtil.update_user_avatar(dict["user_id"],dict["pic_id"])
    dict2={status:"1","TOF":status}
    return json.dumps(dict2)

@vuser.route("/get_user_recommendation_list/<user_id>")
def recommendation(user_id):
    list = []
    exp = 'none'
    id_list = []
    tag_list=[]
    now = datetime.now()
    try:
        list = DBUtil.retrieve_user_activities(user_id)
        for act in list:
            if act.is_canceled == 0 and now<act.end_date:
                id_list.append(act.id)
                tag_list.append(act.tags.strip().split(","))

    except:
        exp='failed'
    dictlist = GETData(tag_list)
    slist = dictlist.keys()
    labellist = []
    for set in slist:
        if dictlist[set] > 0.6:
            for i in set:
                labellist.append(i)
                break
    labellist = list(set(labellist))
    l2 = []
    [l2.append(i) for i in labellist if not i in l2]
    joinedlist=DBUtil.retrieve_user_activities(user_id)
    grouplist=DBUtil.retrieve_user_groups(user_id)
    alllist=[]
    for g in grouplist:
        alllist.append(DBUtil.retrieve_activitiy_by_group(g.id,datetime.now() - timedelta(days=2), 999))
    actlist=[]
    for a in alllist:
        if a not in actlist and a.is_canceled==0 and a not in joinedlist:
            actlist.append(a)
    newlist=[]
    for act in actlist:
        str = act.tags.strip()
        c_taglist = str.split(",")
        for t in c_taglist:
            if t in l2:
                newlist.append(act)
    idlist=[]
    for act in newlist:
        if act.id not in idlist:
            idlist.append(act.id)
    dict2 = {'status': '1', 'result': idlist, 'errcode': "none"};
    return json.dumps(dict2)


@vuser.route("/testrecom")
def testrecom():
    id_list = []
    tag_list = []
    list=DBUtil.retrieve_activitiy_by_group(2, datetime.datetime.now() - timedelta(days=200), 999)
    for act in list:
        if act.is_canceled == 0 :
            id_list.append(act.id)
            tag_list.append(act.tags.strip().split(","))
    dictlist=GETData(tag_list)
    slist=dictlist.keys()
    labellist=[]
    for set in slist:
        if dictlist[set]>0.6:
         for i in set:
             labellist.append(i)
             break
    print(labellist)
    print(type(labellist[0]))
    l2 = []
    [l2.append(i) for i in labellist if not i in l2]
    print(l2)
    return("fuck")


