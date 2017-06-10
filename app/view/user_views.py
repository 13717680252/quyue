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
        dict["birthdate"]  = dict['birthdate'].strftime('%Y-%m-%d')
        dict['status']='1'
        list,error=DBUtil.retrieve_user_friendslist(user_id)
        list=list.strip()
        list = list.split(",")
        list2=[]
        for i in list:
            if i not in list2:
                list2.append(i)
        dict["friendlist"]=list2
    print(dict)
    return (json.dumps(dict))


@vuser.route('/get_user_friend_activities/<user_id>',methods=['POST'])
def get_friend_activities(user_id):
    list,ret=DBUtil.retrieve_user_friendslist(user_id)
    str = list.strip()
    list= str.split(",")
    actlist=[]
    for u in list:
        alist = DBUtil.retrieve_user_activities(u)
        for a in alist:
         if a.id not in actlist:
            actlist.append(a.id)
    dict = {'status': '1', 'activity': actlist, 'errcode': "none"};
    return json.dumps(dict)


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

@vuser.route("/change_user_avatar",methods=['POST'])
def change_avatar():
    c_request = request.get_data()
    dict = json.loads(c_request)
    status=DBUtil.update_user_avatar(dict["user_id"],dict["pic_id"])
    dict2={status:"1","TOF":status}
    return json.dumps(dict2)


@vuser.route("/get_user_comment_record/<user_id>",methods=['POST'])
def get_user_comment_record(user_id):
    rlist = DBUtil.retrieve_all_comments_for_user(user_id)
    dict = {}
    i = 0
    print(rlist)
    for c in rlist:
        print(type(c))
        # c[4]=datetime.datetime.strftime(c[4], '%Y-%m-%d %H:%M:%S')
        # dict[i] = c
        clist = list(c)
        clist[4] = datetime.datetime.strftime(clist[4], '%Y-%m-%d %H:%M:%S')
        dict[i] = clist
        i = i + 1
    dict["total"] = i
    dict["status"] = 1
    return json.dumps(dict)

@vuser.route("/get_user_recommendation_list/<user_id>",methods=['POST'])
def recommendation(user_id):
    alist = []
    exp = 'none'
    id_list = []
    tag_list = []
    now = datetime.datetime.now()
    try:
        alist = DBUtil.retrieve_user_activities(22)
        for act in alist:
            if act.is_canceled == 0 and now < act.end_date:
                id_list.append(act.id)
                tag_list.append(act.tags.strip().split(","))

    except:
        exp = 'failed'
    dictlist = GETData(tag_list)
    slist = dictlist.keys()
    print("dictlist.keys()")
    print(slist)
    labellist = []
    for mset in slist:
        if dictlist[mset] >= 0.5:
            for i in mset:
                labellist.append(i)
                break
    print(labellist)
    labellist = list(set(labellist))
    l2 = []
    [l2.append(i) for i in labellist if not i in l2]
    joinedlist = DBUtil.retrieve_user_activities(22)
    joinedidlist = []
    for i in joinedlist:
        joinedidlist.append(i.id)
    print(joinedidlist)
    grouplist = DBUtil.retrieve_user_groups(22)
    alllist = []
    for g in grouplist:
        alllist = alllist + (DBUtil.retrieve_activitiy_by_group(g.id, datetime.datetime.now() - timedelta(days=2), 999))
    actlist = []
    for a in alllist:
        if a not in actlist and a.is_canceled == 0 and a.id not in joinedidlist:
            actlist.append(a)
    newlist = []
    for act in actlist:
        str = act.tags.strip()
        c_taglist = str.split(",")
        for t in c_taglist:
            if t in l2:
                newlist.append(act)
    idlist = []
    for act in newlist:
        if act.id not in idlist:
            idlist.append(act.id)
    dict2 = {'status': '1', 'result': idlist, 'errcode': exp};
    return json.dumps(dict2)


@vuser.route("/testrecom")
def testrecom():
        alist = []
        exp = 'none'
        id_list = []
        tag_list = []
        now = datetime.datetime.now()
        try:
            alist = DBUtil.retrieve_user_activities(22)
            for act in alist:
                if act.is_canceled == 0 and now < act.end_date:
                    id_list.append(act.id)
                    tag_list.append(act.tags.strip().split(","))

        except:
            exp = 'failed'
        dictlist = GETData(tag_list)
        slist = dictlist.keys()
        print("dictlist.keys()")
        print(slist)
        labellist = []
        for mset in slist:
            if dictlist[mset] >= 0.5:
                for i in mset:
                    labellist.append(i)
                    break
        print(labellist)
        labellist = list(set(labellist))
        l2 = []
        [l2.append(i) for i in labellist if not i in l2]
        joinedlist = DBUtil.retrieve_user_activities(22)
        joinedidlist=[]
        for i in joinedlist:
            joinedidlist.append(i.id)
        print(joinedidlist)
        grouplist = DBUtil.retrieve_user_groups(22)
        alllist = []
        for g in grouplist:
            alllist=alllist+(DBUtil.retrieve_activitiy_by_group(g.id, datetime.datetime.now() - timedelta(days=2), 999))
        actlist = []
        for a in alllist:
            if a not in actlist and a.is_canceled == 0 and a.id not in joinedidlist:
                actlist.append(a)
        newlist = []
        for act in actlist:
            str = act.tags.strip()
            c_taglist = str.split(",")
            for t in c_taglist:
                if t in l2:
                    newlist.append(act)
        idlist = []
        for act in newlist:
            if act.id not in idlist:
                idlist.append(act.id)
        print(idlist)
        return("sb")

