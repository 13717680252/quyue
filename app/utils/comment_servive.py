from app.model.DBUtil import *
def user_comment(args):
    user=args['commed_user_id']
    level=args['level']
    userinfo=DBUtil.retrieve_userinfo_by_id(user)
    if level==1:
     userinfo['credict']=userinfo['credict']-5
    else:
     userinfo['credict'] = userinfo['credict'] +5*level
    states,exp=DBUtil.update_userinfo(user,userinfo)
    return states

def activity_comment(args):
    act=args['act_id']
    level=args['level']
    list=[]
    states=[]
    list=DBUtil.retrieve_joined_people_of_activity(act)
    for i in list:
        userinfo = DBUtil.retrieve_userinfo_by_id(i)
        if level == 1:
            userinfo['credict'] = userinfo['credict'] - 1
        else:
            userinfo['credict'] = userinfo['credict'] + 1 * level
        state, exp = DBUtil.update_userinfo(i, userinfo)
        states.append(state)
    return states




