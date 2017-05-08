from app.model.DBUtil import *
from app.model.models import TActivity
import datetime
import re
from datetime import  timedelta
def searchactivity(groupid,lables,keyword):
    list = DBUtil.retrieve_activitiy_by_group(groupid, datetime.now() - timedelta(days=200), 999)
    idlist=[]
    newlist=[]
    for act in list:
        idlist.append[act.id]
    for i in idlist:
        act = DBUtil.retrieve_activity_by_id(i)
        str = act.tags.strip()
        c_taglist = str.split(",")
        for j in c_taglist:
            if j in lables:
                newlist.append(i)
        str=act.description
        if keyword in str:
            newlist.append(i)
    result = [x for x in newlist if newlist.count(x) == 1]
    return result

def searchfriend(keyword):
    pass







