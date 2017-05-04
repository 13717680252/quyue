'''
Created on 2017年4月14日
@author: KarlMical
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from app.model.models import TUser, TGroup, TActivity, TCommentActivity, TCommnetPerson
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.expression import exists, select
from sqlalchemy.sql.elements import or_, literal
import redis


url_host = 'localhost'
url_port = '3306'
url_database = 'yue'
url_username = 'root'
url_pwd = 'hos950928'
db_url = (
    'mysql://' +
    url_username + ':' + url_pwd + '@' +
    url_host + ':' + url_port +'/' +
    url_database + '?charset=utf8'
    )

engine = create_engine(db_url, encoding='utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
#
#redis key patterns
k_user_act = "user:%s:activities"   #actviites which the user joined
k_user_group = "user:%s:groups"     #groups which the user attention

#redis instance
rins = redis.Redis(host='localhost', port=6379, password='redis',db=1)

class DBUtil:
    @staticmethod
    def exec_query(handle_func, **args):
        ss = DBSession()
        rs = handle_func(ss, args)
        ss.close()
        return rs


    @staticmethod
    def exec_query_with_conn(handle_func, **args):
        conn = engine.connect()
        rs = handle_func(conn, args)
        conn.close()
        return rs


    @staticmethod
    def __decode_list_with_utf8(blist):
        '''
        decode a binary list with utf8
        :param blist:
        :return: a list of strings
        '''
        ul = []
        for item in blist:
            ul.append(item.decode('utf8'))
        return ul


    @staticmethod
    def __util_check_user_name_duplicated(ss, args):
        try:
            rs = ss.query(TUser.id).filter(TUser.name == args['username']).limit(1).count()
        except Exception as e:
            print(e)
            return False, e

        return (rs == 1), None


    @staticmethod
    def __util_check_user_phone_duplicated(ss, args):
        try:
            rs = ss.query(TUser.id).filter(TUser.phone == args['phonenumber']).limit(1).count()
        except Exception as e:
            print(e)
            return False, e
        return (rs == 1), None


    @staticmethod
    def __util_check_user_mail_duplicate(ss, args):
        try:
            rs = ss.query(TUser.id).filter(TUser.mail == args['mail']).limit(1).count()
        except Exception as e:
            print(e)
            return False, e
        return (rs == 1), None


    @staticmethod
    def __util_check_user_mail_and_psw(ss, args):
        mail = args['mail']
        psw = args['psw']
        try:
            rs = ss.query(TUser.id).filter(TUser.mail == mail, TUser.password == psw).limit(1).count()
        except Exception as e:
            print(e)
            return False, e
        return True, None


    @staticmethod
    def __util_check_mail_activate(ss, args):
        mail = args['mail']
        try:
            rs = ss.query(TUser.is_activated).filter(TUser.mail == mail).limit(1).one()
        except Exception as e:
            print(e)
            return False, e
        return (rs[0] == 'y'), None


    @staticmethod
    def __util_retrieve_user_friends(ss, args):
        try:
            rs = ss.query(TUser.friends).filter(TUser.id == args['user_id']).first()
        except Exception as e:
            print(e)
            return None, e

        return rs[0], None


    @staticmethod
    def __util_retrieve_activity(ss, args):
        try:
            item = ss.query(TActivity).filter(TActivity.id == args['id']).first()
            ss.expunge(item)
            ss.commit()
        except Exception as e:
            print(e)
            return None

        return item


    @staticmethod
    def __util_retrieve_group(ss, args):
        try:
            group = ss.query(TGroup).filter(TGroup.id == args['id']).first()
            ss.expunge(group)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return None

        return group


    @staticmethod
    def __util_retrieve_activity_by_group(ss, args):
        gid = args['group_id']
        limit = args['limit']
        after_date = args['after_date']
        print(after_date)
        print(type(after_date))
        try:
            rs = ss.query(TActivity).filter(TActivity.group_id == gid, TActivity.create_date >= after_date).limit(limit).all()
            ss.expunge_all()
            ss.commit()
        except Exception as e:
            print(e)
            return None

        return rs



    @staticmethod
    def __util_insert_new_user(conn, args):
        tb = TUser.__table__
        pcolumns = [tb.c.id, tb.c.name, tb.c.password, tb.c.mail, tb.c.phone,
                    tb.c.stu_id, tb.c.college, tb.c.profession, tb.c.sex,
                    tb.c.birthdate, tb.c.avatar, tb.c.is_activated]
        vals = [ literal(None), literal(args['name']), literal(args['password']), literal(args['mail']),
                  literal(args['phone']), literal(args['stu_id']), literal(args['college']),
                  literal(args['profession']), literal(args['sex']), literal(args['birthdate']),literal(args['avatar']), literal(args['is_activated'])]
        sel = select(vals).\
            where(~exists(select(
                [tb.c.id],
                or_(tb.c.name == args['name'], tb.c.mail == args['mail']))
                          )
                  )
        ins = tb.insert().from_select(pcolumns,sel)
        #print(ins)
        try:
            rs = conn.execute(ins)
        except Exception as e:
            print(e)
            return 0, e

        return rs.lastrowid, None


    @staticmethod
    def __util_insert_new_group(ss, args):
        #print('insert new group')
        new_group = TGroup(name=args['name'], type=args['type'], description=args['description'], create_date=args['create_date'])
        try:
            ss.add(new_group)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return 0, e

        return new_group.id, None


    @staticmethod
    def __util_insert_new_activity(ss, args):
        #print('insert a new activity')
        new_activity = TActivity(name=args['name'], publisher=args['publisher'], group_id=args['group_id'],
                                 description=args['description'], start_date=args['start_date'], end_date=args['end_date'],
                                 min_num=args['min_num'], max_num=args['max_num'], cur_num=args['cur_num'], join_ids=args['join_ids'],
                                 tags=args['tags'], is_canceled=args['is_canceled'])
        try:
            ss.add(new_activity)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return 0, e

        return new_activity.id, None


    @staticmethod
    def __util_insert_activity_comment(ss, args):
        #print()
        comm_act = TCommentActivity(activity_id=args['act_id'], comment_user_id=args['user_id'], level=args['level'],
                                    content=args['content'])
        try:
            ss.add(comm_act)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return 0, e

        return comm_act.id, None


    @staticmethod
    def __util_insert_comment_person(ss, args):
        #print()
        #TCommnetPerson.commented_user_id
        commp = TCommnetPerson(activity_id=args['act_id'], comment_user_id=args['comm_user_id'], commented_user_id=args['commed_user_id'],
                               level=args['level'], content=args['content'])
        try:
            ss.add(commp)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return 0, e

        return commp.id, None


    @staticmethod
    def __util_add_user_frends(ss, args):
        new_friends = args['new_friends']
        old_friends, exp = DBUtil.__util_retrieve_user_friends(ss, {"user_id": args['user_id']})
        if old_friends is None:
            return False, None

        update_freindslist = ','.join(new_friends)
        if old_friends:
           update_freindslist = old_friends + ',' + update_freindslist
        try:
            ss.query(TUser).filter(TUser.id == args['user_id']).update({TUser.friends : update_freindslist}, synchronize_session=False)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False, e

        return True, None


    @staticmethod
    def __util_update_user_mail_state(ss, args):
        if args['state']:
            ins = 'y'
        else:
            ins = 'n'
        mail = args['mail']
        try:
            ss.query(TUser).filter(TUser.mail == mail).update({TUser.is_activated : ins}, synchronize_session=False)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False, e

        return True, None


    @staticmethod
    def flush_redis():
        '''
        remove all data of redis database, only for test
        :return:
        '''
        rins.flushdb()


    #param 'name': the name of user
    #return a tuple <isExisted, error>
    #'isExisted' is a boolean indicates whether the user name is already existed;
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def check_user_name_duplicated(name):
        return DBUtil.exec_query(DBUtil.__util_check_user_name_duplicated, username=name)


    #param 'phone': the phone number of user
    #return a tuple <isExisted, error>
    #'isExisted' is a boolean indicates whether the user's phone number is already existed;
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def check_user_phone_duplicated(phone):
        return DBUtil.exec_query(DBUtil.__util_check_user_phone_duplicated, phonenumber=phone)


    #param 'mail': the mail address of user
    #return a tuple <isExisted, error>
    #'isExisted' is a boolean indicates whether the user's mail address is already existed;
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def check_user_mail_duplicated(mail):
        return DBUtil.exec_query(DBUtil.__util_check_user_mail_duplicate, mail=mail)


    @staticmethod
    def check_user_mail_and_psw(mail, psw):
       '''
       :param mail: mail address
       :param psw: password
       :return: a tuple <pass, error>
            'pass' is boolean value indicates that whether mail and psw are matched
            'error' is the exception when executing the query in the database, None means no exception
       '''
       return DBUtil.exec_query(DBUtil.__util_check_user_mail_and_psw, mail=mail, psw=psw)


    @staticmethod
    def check_mail_activate(mail):
        '''
        :param mail: mail address
        :return: a tuple <ok, error>
            'ok' is boolean value indicates that whether the mail is activated
            'error' is the exception when executing the query in the database, None means no exception
        '''
        return DBUtil.exec_query(DBUtil.__util_check_mail_activate, mail=mail)

    #param 'user_id': the id of query user
    #return a tuple <friendslist, error>
    #'friendslist': if successfully retrieved, friendslist is a str; else None
    #'error':  the exception when executing the query in the database, None means no exception
    @staticmethod
    def retrieve_user_friendslist(user_id):
        return DBUtil.exec_query(DBUtil.__util_retrieve_user_friends, user_id=user_id)


    @staticmethod
    def retrieve_user_activities(user_id):
        '''
        get a list of activities which the user joined
        :param user_id: id of the user
        :return:  a list of activities
        '''
        k = k_user_act % user_id
        act_ids = DBUtil.__decode_list_with_utf8(rins.smembers(k))
        activities = []
        ss = DBSession()
        for id in act_ids:
            act = DBUtil.__util_retrieve_activity(ss, {'id': id})
            if act is not None:
                activities.append(act)
        ss.close()
        return  activities


    @staticmethod
    def retrieve_user_groups(user_id):
        '''
        get the groups that the user attention
        :param user_id: id of the user
        :return: a list of groups
        '''
        gids = DBUtil.__decode_list_with_utf8(rins.smembers(k_user_group % user_id))
        gl = []
        ss = DBSession()
        for id in gids:
            group = DBUtil.__util_retrieve_group(ss, {'id': id})
            if group is not None:
                gl.append(group)
        ss.close()
        return gl


    @staticmethod
    def retrieve_activity_by_id(id):
        '''
        retrieve a activity by its id
        :param id: id of the activity
        :return: an activity if the id is valid or None otherwise
        '''
        return  DBUtil.exec_query(DBUtil.__util_retrieve_activity, id=id)


    @staticmethod
    def retrieve_activitiy_by_group(group_id, after_date, limit):
        '''
        retrieve a list of activities with max_num by the group id
        :param group_id: id of refered group
        :param after_date: a date that activities' published date should be after it
        :param limit: limit number of activities to be retrieved
        :return: a list of activities
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_activity_by_group, group_id=group_id, after_date=after_date, limit=limit)


    @staticmethod
    def retrieve_group_by_id(id):
        '''
        retrieve a group by its id
        :param id: id of the group
        :return: a group
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_group, id = id)


    #param 'args': a dict of user propertities
    #reutrn a tuple <rowid, error>
    #'rowid' is the last user row id, if not exists, rowid is 0
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def insert_new_user(args):
        return DBUtil.exec_query_with_conn(DBUtil.__util_insert_new_user,
                          name=args['name'], password=args['password'], mail=args['mail'],
                          phone=args['phone'], stu_id=args['stu_id'], college=args['college'],
                          profession=args['profession'], sex=args['sex'],
                          birthdate=args['birthdate'], avatar=args.get('avatar'), is_activated=args.get('is_activated'))


    #param 'args': a dict of group propertities
    #return a tuple <groupid, error>
    #'groupid' is group id of new group inserted. If failed, group id is 0
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def insert_new_group(args):
        return DBUtil.exec_query(DBUtil.__util_insert_new_group, name=args['name'], type=args.get('type'),
                                 description=args['description'], create_date=args['create_date'])


    #param 'args': a dict of group properties
    # return a tuple <activity_id, error>
    # 'groupid' is id of new activity inserted. If failed, group id is 0
    # 'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def insert_new_activity(args):
        return DBUtil.exec_query(DBUtil.__util_insert_new_activity,
                                 name=args['name'], publisher=args['publisher'], group_id=args['group_id'],
                                 description=args['description'], start_date=args['start_date'], end_date=args['end_date'],
                                 min_num=args['min_num'], max_num=args['max_num'], is_canceled=args['is_canceled'],cur_num=args.get('cur_num'),
                                 join_ids=args.get('join_ids'), tags=args.get('tags'))

    #param 'args': a dict of commentOfActivity properties
    # return a tuple <commnet_id, error>
    # 'comment_id' is id of new comment inserted. If failed, commnet_id is 0
    # 'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def insert_new_comment_activity(args):
        return DBUtil.exec_query(DBUtil.__util_insert_activity_comment,
                                 act_id=args['act_id'], user_id=args['user_id'], level=args['level'], content=args['content'])


    # param 'args': a dict of commentOfPerson properties
    # return a tuple <comment_id, error>
    # 'comment_id' is id of new comment inserted. If failed, commnet_id is 0
    # 'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def insert_new_comment_person(args):
        return DBUtil.exec_query(DBUtil.__util_insert_comment_person,
                                 act_id=args['act_id'],comm_user_id=args['comm_user_id'], commed_user_id=args['commed_user_id'],
                                 level=args['level'], content=args['content'])


    @staticmethod
    def join_activity(user_id, activity_id_list):
        '''
        :param user_id:
        :param activity_id_list:
        :return:
        '''
        k = k_user_act % user_id
        for id in activity_id_list:
            rins.sadd(k, id)


    @staticmethod
    def add_user_group(user_id, groups):
        '''
        add an id list of groups to user
        :param groups: an id list
        :return:  the number of groups that were added, not including the ones that were present
        '''
        return rins.sadd(k_user_group % user_id, *groups)


    @staticmethod
    def update_user_friends(user_id, new_friends):
        '''
        :param user_id:
        :param new_friends: a str list of user id
        :return: a tuple <ok, error>
            'ok': a boolean value indicates whether th update is successful.
            'error' is the exception when executing the query in the database, None means no exception
        '''
        return DBUtil.exec_query(DBUtil.__util_add_user_frends, user_id=user_id, new_friends=new_friends)


    @staticmethod
    def update_user_mail_state(mail, state):
        '''
        :param mail: mail address
        :param state: mail's activate sate, True if activated, False if not activated
        :return: a tuple <ok, error>
            'ok': a boolean value indicates whether th update is successful.
            'error': the exception when executing the query in the database, None means no exception
        '''
        return DBUtil.exec_query(DBUtil.__util_update_user_mail_state, mail=mail, state=state)


    @staticmethod
    def remove_user_activities(user_id, activity_ids):
        '''
        remove a list of activies which the user joined
        :param user_id: id of the user
        :param activity_ids: the id list of activities
        :return:  the number of activities that were removed
        '''
        return  rins.srem(k_user_act % user_id, *activity_ids)