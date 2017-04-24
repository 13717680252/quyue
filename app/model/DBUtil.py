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

url_host = 'localhost'
url_port = '3306'
url_database = 'yue'
url_username = 'hos950928'
url_pwd = ''
db_url = (
    'mysql://' +
    url_username + ':' + url_pwd + '@' +
    url_host + ':' + url_port +'/' +
    url_database + '?charset=utf8'
    )

engine = create_engine(db_url, encoding='utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

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
    def __util_retrieve_user_friends(ss, args):
        try:
            rs = ss.query(TUser.friends).filter(TUser.id == args['user_id']).first()
        except Exception as e:
            print(e)
            return None, e

        return rs[0], None

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


    #param 'user_id': the id of query user
    #return a tuple <friendslist, error>
    #'friendslist': if successfully retrieved, friendslist is a str; else None
    #'error':  the exception when executing the query in the database, None means no exception
    @staticmethod
    def retrieve_user_friendslist(user_id):
        return DBUtil.exec_query(DBUtil.__util_retrieve_user_friends, user_id=user_id)


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


    #param 'user_id'
    #param 'new_friends': a str list of user id
    #return a tuple <ok, error>
    #'ok': a boolean value indicates whether th update is successful.
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def update_user_friends(user_id, new_friends):
        return DBUtil.exec_query(DBUtil.__util_add_user_frends, user_id=user_id, new_friends=new_friends)