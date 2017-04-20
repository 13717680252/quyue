'''
Created on 2017年4月14日
@author: KarlMical
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from models import TUser, TGroup, TActivity
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.expression import exists, select
from sqlalchemy.sql.elements import or_, literal

url_host = 'localhost'
url_port = '3307'
url_database = 'date'
url_username = 'root'
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
    def __util_check_user_phone_dupliacted(ss, args):
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
        print('insert a new activity')
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
        return DBUtil.exec_query(DBUtil.__util_check_user_phone_dupliacted, phonenumber=phone)


    #param 'mail': the mail address of user
    #return a tuple <isExisted, error>
    #'isExisted' is a boolean indicates whether the user's mail address is already existed;
    #'error' is the exception when executing the query in the database, None means no exception
    @staticmethod
    def check_user_mail_duplicated(mail):
        return DBUtil.exec_query(DBUtil.__util_check_user_mail_duplicate, mail=mail)

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
