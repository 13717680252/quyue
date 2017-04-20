'''
Created on 2017年4月16日

@author: KarlMical
'''

from DBUtil import DBUtil
from datetime import  datetime
import  time

def check_user_name(name):
    #check whether user name 'fsx' is already existd
    isExisted, exp = DBUtil.check_user_name_duplicated(name)
    if isExisted:
        print("'%s' is a duplicated user name!" % name);
    else:
        print("'%s' is not an existed user name!" % name, exp);

def check_user_phone(phone):  
    #check whether user phone number '123456' is already existd
    isExisted, exp = DBUtil.check_user_phone_duplicated(phone)
    if isExisted:
        print("'%s' is a duplicated user phone number!" % phone)
    else:
        print("'%s' is not an existed user phone number!" % phone, exp);

def check_user_mail(mail):
    #check whether user mail address '123@qq.com' is already existd
    isExisted, exp = DBUtil.check_user_mail_duplicated(mail)
    if isExisted:
        print("'%s' is a duplicated user mail address!" % mail);
    else:
        print("'%s' is not an existed user mail address!" % mail, exp);

def insert_new_user(new_user):
    uid, exp = DBUtil.insert_new_user(new_user)
    if uid is not 0:
        print("user is created, id is '%d'" % uid)
    else:
        print('user added failed!', exp)

def insert_new_group(new_group):
    group_id, exp = DBUtil.insert_new_group(new_group)
    if group_id is not 0:
        print("A new group is added, id is '%d'" % group_id, new_group)
    else:
        print("The group is failed to be added!", exp, new_group)

def insert_new_activity(activity):
    actid, exp = DBUtil.insert_new_activity(activity)
    if actid is not 0:
        print("A new activity is added, id is '%d'" % actid, activity)
    else:
        print("The activity is failed to be added!", activity)


def insert_new_comment_acticity(comment):
    cid, exp = DBUtil.insert_new_comment_activity(comment)
    if cid is not 0:
        print("A new commnet has been added, id is '%d'" % cid, comment)
    else:
        print("The comment failed to be added!", comment)


def insert_new_comment_person(comment):
    cid, exp = DBUtil.insert_new_comment_person(comment)
    if cid is not 0:
        print("A new comment of the person has been added, is is '%d'" % cid, comment)
    else:
        print("The comment failed to be added!", comment)

def get_friendslist(user_id):
    friendslist, exp = DBUtil.retrieve_user_friendslist(user_id=user_id)
    if friendslist is not None:
        print("Got the friends list of user '%d': '%s'!" % (user_id, friendslist))
    else:
        print("Failed to get the friends list of user '%d'!" % user_id)


def add_friends(user_id, friends):
    ok, exp = DBUtil.update_user_friends(user_id, friends)
    if ok:
        print("New friends are added for user '%d'!" % user_id, friends)
    else:
        print("Failed to add friends for user '%d'!" % user_id, friends)

'''
check_user_name('fsx')
check_user_phone('123456')
check_user_mail('123@qq.com') 
#sex: 'm' or 'f'
#is_activated: 'n' or 'y', optional
new_user = {"name" : 'f5d8', "password" : '123456', "mail" : '153@qq.com',
            "phone" : '123456', "stu_id" : '123456', "college": '北交大',
            "profession": 'xxx', "sex": 'm', "birthdate": "1996-01-01", "is_activated":'n'}
insert_new_user(new_user)

#insert a new group
new_group1 = {"name": 'xx读书会', "type" : 1, "description": "用户自定义组", "create_date": "2017-04-01"}
new_group2 = {"name": '篮球', "description": "系统自定义组", "create_date": "2017-04-01"}
insert_new_group(new_group1)
insert_new_group(new_group2)


#insert an activity
#field 'cur_num', 'join_ids' and 'tags' are optional
s = datetime.now() #a timestamp denotes the start time of the act
e = datetime.now()  #a timesatmp denotes end time of the act
activity = {"name": '新活动', "publisher": 8, "group_id": 1, "description": 'a description',
            "start_date": s, "end_date": e, "min_num": 2, "max_num": 10, "cur_num": 3,
            "join_ids":'1,5,8', "tags":'聚餐,交友', "is_canceled": 0}
insert_new_activity(activity)
'''

#day 04-20
#insert a new commnet of the activity
'''
new_commentOfActivity = {"act_id": 1, "user_id": 2, "level": 2, "content": 'xxx'}
insert_new_comment_acticity(new_commentOfActivity)
'''


#insert a new commnet of the person
'''
new_commnetOfPerson = {"act_id": 1, "comm_user_id": 1, "commed_user_id": 8, "level": 5, "content": "Karl is a kind person"}
insert_new_comment_person(new_commnetOfPerson)
'''

#retrieve the friends list of a user
'''
get_friendslist(4)
'''

#add friends
'''
add_friends(4, ['1', '8', '9'])
'''