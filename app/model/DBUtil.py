from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from app.model.models import TUser, TGroup, TActivity, TCommentActivity, TCommnetPerson,TPicUrl, t_t_chat
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.expression import exists, select
from sqlalchemy.sql.elements import or_, literal, and_
import redis
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
k_act_pic = "act:%s:pic"            #picture ids upload for an activity
k_user_act = "user:%s:activities"   #actviites which the user joined
k_user_group = "user:%s:groups"     #groups which the user attention

#redis instance
rins = redis.Redis(host='localhost', port=6379, password='',db=1)

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
    def __util_retrieve_userid_by_name(ss, args):
        try:
            rs = ss.query(TUser.id).filter(TUser.name == args['name']).limit(1).first()
        except Exception as e:
            print(e)
            return -1

        if rs is None:
            # name not found
            return 0
        return rs[0]


    @staticmethod
    def __util_retrieve_userid_by_email(ss, args):
        try:
            rs = ss.query(TUser.id).filter(TUser.mail == args['mail']).limit(1).first()
        except Exception as e:
            print(e)
            return -1

        if rs is None:
            # mail not found
            return 0
        return rs[0]


    @staticmethod
    def __util_retrieve_user_friends(ss, args):
        try:
            rs = ss.query(TUser.friends).filter(TUser.id == args['user_id']).first()
        except Exception as e:
            print(e)
            return None, e

        return rs[0], None


    @staticmethod
    def __util_retrieve_userinfo_by_id(ss, args):
        try:
            rs = ss.query(TUser.name, TUser.mail, TUser.active_value, TUser.avatar, TUser.birthdate, TUser.college,
                          TUser.is_activated, TUser.credit, TUser.phone, TUser.profession, TUser.sex, TUser.stu_id).\
                    filter(TUser.id == args['id']).limit(1).first()
            ss.commit()
        except Exception as e:
            print(e)
            return None

        if rs is None:
            return None
        d = {}
        d['name'] = rs[0]
        d['mail'] = rs[1]
        d['act_v'] = rs[2]
        d['ava'] = rs[3]
        d['birthdate'] = rs[4]
        d['college'] = rs[5]
        d['is_act'] = rs[6]
        d['credict'] = rs[7]
        d['phone'] = rs[8]
        d['profession'] = rs[9]
        d['sex'] = rs[10]
        d['stu_id'] = rs[11]
        return  d


    @staticmethod
    def __util_retrieve_avatar_url(ss, args):
        try:
            rs = ss.query(TPicUrl.url).filter(TPicUrl.pic_id == args["id"]).first()
        except Exception as e:
            print(e)
            return  None
        if rs is None:
            return None
        return rs[0]


    @staticmethod
    def __util_retrieve_user_avatar(ss, args):
        try:
            rs = ss.query(TUser.avatar).filter(TUser.id == args["id"]).first()
        except Exception as e:
            print(e)
            return None
        # print(rs)
        if rs is None:
            return None
        return rs[0]


    @staticmethod
    def __util_retrieve_all_userid(ss, args):
        try:
            rs = ss.query(TUser.id).all()
        except Exception as e:
            print(e)
            return None
        ret = []
        for item in rs:
            ret.append(item[0])
        return  ret


    @staticmethod
    def __util_retrieve_all_comments_for_user(ss, args):
        try:
            pass
            rs = ss.query(TCommnetPerson.comment_user_id, TCommnetPerson.activity_id, TCommnetPerson.content,
                     TCommnetPerson.level, TCommnetPerson.create_date).\
                    filter(TCommnetPerson.commented_user_id == args["user_id"], TCommnetPerson.is_deleted == 0).all()
        except Exception as e:
            print(e)
            return None

        # print(rs)
        return rs



    @staticmethod
    def __util_retrieve_activity(ss, id):
        try:
            item = ss.query(TActivity).filter(TActivity.id == id).first()
            ss.expunge(item)
            ss.commit()
        except Exception as e:
            print(e)
            return None

        return item


    @staticmethod
    def __util_retrieve_joined_people_of_activity(ss, args):
        try:
            rs = ss.query(TActivity.join_ids).filter(TActivity.id == args['id']).limit(1).first()
        except Exception as e:
            print(e)
            return None

        if rs is None or len(rs) is 0:
            return None
        return rs[0]


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
        try:
            rs = ss.query(TActivity).filter(TActivity.group_id == gid, TActivity.create_date >= after_date).limit(limit).all()
            ss.expunge_all()
            ss.commit()
        except Exception as e:
            print(e)
            return None

        return rs


    @staticmethod
    def __util_retrieve_chat_info(conn, args):
        sql = select([t_t_chat.c.chat_info, t_t_chat.c.chat_data]).\
            where(and_(
                t_t_chat.c.send_id == args['send_id'],
                t_t_chat.c.get_id == args['get_id'],
                t_t_chat.c.is_clear == 0
                )
            )
        update_sql = t_t_chat.update().\
            where(and_(
                t_t_chat.c.send_id == args['send_id'],
                t_t_chat.c.get_id == args['get_id'],
                t_t_chat.c.is_clear == 0
            )
        ).values(is_clear=1)
        ret = []
        trans = conn.begin()
        try:
            rs = conn.execute(sql)
            # not hit, return empty list
            if rs.rowcount is 0:
                return ret
            # update the is_clear field
            # print(update_sql)
            conn.execute(update_sql)
            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            return None

        for r in rs:
            ret.append((r['chat_info'], r['chat_data']))
        return ret


    @staticmethod
    def __util_retrieve_chat_send_id(conn, args):
        pass
        get_id = args['get_id']
        sql = select([t_t_chat.c.send_id]).where(
            and_(
                t_t_chat.c.get_id == get_id,
                t_t_chat.c.is_notify == 0
            )
        )
        update_sql = t_t_chat.update(). \
            where(and_(
                t_t_chat.c.get_id == get_id,
                t_t_chat.c.is_notify == 0
        )
        ).values(is_notify=1)
        ret = []
        trans = conn.begin()
        try:
            rs = conn.execute(sql)
            if rs.rowcount is 0:
                return ret
            # update the is_notify field
            conn.execute(update_sql)
            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            return None

        for r in rs:
            ret.append(r[0])
        return ret


    @staticmethod
    def __util_retrieve_pic_count(ss, args):
        try:
            rs = ss.query(TPicUrl).count()
        except Exception as e:
            print(e)
            return -1

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
            ss.query(TGroup).filter(TGroup.id == args['group_id']).\
                update({TGroup.activetity_count : TGroup.activetity_count + 1}, synchronize_session=False)
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
    def __util_insert_pic_url(ss, args):
        tpic = TPicUrl(url=args["url"])
        try:
            ss.add(tpic)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return None

        return tpic.pic_id


    @staticmethod
    def __util_insert_new_chat(conn, args):
        ins = t_t_chat.insert().values(get_id=args['get_id'], send_id=args['send_id'], chat_info=args['chat_info'])
        try:
            conn.execute(ins)
        except Exception as e:
            print(e)
            return False

        return True


    @staticmethod
    def __util_increase_group_attention(ss, group_id, inc=1):
        '''
        increase the group attention by number 'inc'
        :param ss: db session
        :param group_id: group id
        :param inc: number of attention to increase
        :return: True if success, False otherwise
        '''
        try:
            rs = ss.query(TGroup).filter(TGroup.id == group_id).\
                update({TGroup.attention_count : TGroup.attention_count + inc}, synchronize_session=False)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False

        # print("rs",rs, "inc", inc)
        if rs is None or rs is not 1:
            return False
        return  True


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
    def __util_join_activity(ss, user_id, act_id):
        '''
        :param ss: db session
        :param user_id: the user id
        :param act_id:  the id of activity to be joined
        :return: True if the joined user if updated in the activity joined list, False if failed
        '''
        jl = DBUtil.retrieve_joined_people_of_activity(act_id)
        if jl is None:
            return False
        #check if the user is already joined
        for id in jl:
            if id is user_id:
                return True
        #add to joined list
        jl.append(user_id)
        jl_str = ','.join(jl)
        try:
            rs = ss.query(TActivity).filter(TActivity.id == act_id, TActivity.max_num >= len(jl)).\
                        update({TActivity.join_ids : jl_str, TActivity.cur_num : TActivity.cur_num + 1}, synchronize_session=False)
            #
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False

        if rs is 1:
            return True
        return False


    @staticmethod
    def __util_update_user_mail_state(ss, args):
        if args['state']:
            ins = 'y'
        else:
            ins = 'n'
        mail = args['mail']
        try:
            rs = ss.query(TUser).filter(TUser.mail == mail).update({TUser.is_activated : ins}, synchronize_session=False)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False, e

        if rs is 1:
            return True, None
        return False, None


    @staticmethod
    def __util_update_userinfo(ss, args):
        info = args['info']
        update_info = {}
        if info.get('name'):
            update_info[TUser.name] = info['name']
        if info.get('mail'):
            update_info[TUser.mail] = info['mail']
        if info.get('phone'):
            update_info[TUser.phone] = info['phone']
        if info.get('stu_id'):
            update_info[TUser.stu_id] = info['stu_id']
        if info.get('college'):
            update_info[TUser.college] = info['college']
        if info.get('profession'):
            update_info[TUser.college] = info['profession']
        if info.get('sex'):
            update_info[TUser.sex] = info['sex']
        if info.get('birthdate'):
            update_info[TUser.birthdate] = info['birthdate']
        if info.get('credict'):
            update_info[TUser.credit] = info['credict']
        if info.get('act_v'):
            update_info[TUser.active_value] = info['act_v']
        if info.get('ava'):
            update_info[TUser.avatar] = info['ava']
        if info.get('is_act'):
            update_info[TUser.is_activated] = info['is_act']

        # print(update_info)
        try:
            rs = ss.query(TUser).filter(TUser.id == args['id']).update(update_info, synchronize_session='evaluate')
            # print(rs)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False, e

        if rs is 1:
            return True, None
        return False, None


    @staticmethod
    def __util_update_user_avatar(ss, args):
        try:
            rs = ss.query(TUser).filter(TUser.id == args["user_id"]).\
                update({TUser.avatar : args["avatar_id"]}, synchronize_session=False)
            ss.commit()
        except Exception as e:
            print(e)
            ss.rollback()
            return False

        if rs is 1:
            return True
        return False


    @staticmethod
    def __util_delete_joined_user_of_activity(ss, act_id, user_id):
        '''
        remove user from the activity
        :param ss: db session
        :param act_id: activity id
        :param user_id: user id
        :return: True if success, False failed
        '''
        jl = DBUtil.retrieve_joined_people_of_activity(act_id)
        # print(jl)
        if jl is None:
            return False
        # check if the user if in the joined list of the activity
        found = False
        for id in jl:
            if id is user_id:
                # remove the user if he is in the joined list
                found = True
                jl.remove(id)
                break
        if found:
            try:
                rs = ss.query(TActivity).filter(TActivity.id == act_id).\
                    update({TActivity.join_ids : ','.join(jl), TActivity.cur_num: TActivity.cur_num - 1},
                           synchronize_session=False)
                ss.commit()
            except Exception as e:
                print(e)
                ss.rollback()
                return False
            if rs is 1:
                return True
            else:
                return  False
        #
        print("The user '%s' is not in the joined list of the activity '%s'" % (user_id, act_id))
        return True


    #
    # @staticmethod@staticmethod
    # def __util_decrease_group_attention(ss, args):
    #     try:
    #         ss.query(TGroup).filter(TGroup.id == args['group_id']).\
    #             update({TGroup.attention_count : TGroup.attention_count - 1}, synchronize_session=False)
    #     except Exception as e:
    #         print(e)

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


    @staticmethod
    def retrieve_userinfo_by_id(id):
        '''
        :param id: user id
        :return: a dict
            {
                'name': name, 'mail' : mail, 'phone': phone, 'stu_id': student id,
                'college' : college, 'profession' : profession, 'sex' : sex, 'birthdate': birthdate,
                'credict" : credict, 'act_v' : activive value, 'ava' : avatar, 'is_act' : is activated
            } if found,
            None if not found,
            None if error occurs
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_userinfo_by_id, id=id)


    #param 'user_id': the id of query user
    #return a tuple <friendslist, error>
    #'friendslist': if successfully retrieved, friendslist is a str; else None
    #'error':  the exception when executing the query in the database, None means no exception
    @staticmethod
    def retrieve_user_friendslist(user_id):
        return DBUtil.exec_query(DBUtil.__util_retrieve_user_friends, user_id=user_id)


    @staticmethod
    def retrieve_userid_by_name(name):
        '''
        get user's id by his name
        :param name: user's nick name
        :return: user's id, -1 if error occurs, 0 if not exists
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_userid_by_name, name=name)


    @staticmethod
    def retrieve_userid_by_mail(mail):
        '''
        get user's id by his mail
        :param mail: user's mail
        :return: user's id, -1 if error occurs, 0 if not exists
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_userid_by_email, mail=mail)


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
            act = DBUtil.__util_retrieve_activity(ss, id)
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
    def retrieve_avatar_url(avatar_id):
        '''
        get user avatar url by the avatar id
        :param user_id:
        :return: the avatar url of the user
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_avatar_url, id=avatar_id)


    @staticmethod
    def retrive_user_avatar(user_id):
        '''
        retrieve user's avatar id
        :param user_id:
        :return: id of the user avatar if success, None if failed
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_user_avatar, id=user_id)


    @staticmethod
    def retrieve_all_userid():
        '''
        :return: a list of user id or None if error occured
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_all_userid)


    @staticmethod
    def retrieve_all_comments_for_user(user_id):
        '''
        get all comments for the user
        :param user_id: id of user
        :return: a list of [ TCommnetPerson.comment_user_id, TCommnetPerson.activity_id, TCommnetPerson.content,
                     TCommnetPerson.level, TCommnetPerson.create_date ]
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_all_comments_for_user, user_id=user_id)


    @staticmethod
    def retrieve_activity_by_id(id):
        '''
        retrieve an activity by its id
        :param id: id of the activity
        :return: an activity if the id is valid or None otherwise
        '''
        ss = DBSession()
        rs = DBUtil.__util_retrieve_activity(ss, id)
        ss.close()
        return  rs


    @staticmethod
    def retrieve_joined_people_of_activity(id):
        '''
        retrieve all joinded people's id by the activity id
        :param id: the activity id
        :return: a list of people id or None if error occured
        '''
        jl =DBUtil.exec_query(DBUtil.__util_retrieve_joined_people_of_activity, id=id)
        if jl is None:
            return None
        if jl is "":
            return []
        return jl.split(',')


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


    @staticmethod
    def retrieve_chat_info(get_id, send_id):
        '''
        retrieve all pairs for chat info that is not cleared
        :param get_id:
        :param send_id:
        :return: [chat_info, chat_data] or None
        '''
        return DBUtil.exec_query_with_conn(DBUtil.__util_retrieve_chat_info,
                                           get_id=get_id, send_id=send_id)


    @staticmethod
    def retrieve_chat_send_id(get_id):
        '''
        get all send id by get id and set the record's is_notify to 1
        :param get_id:
        :return: if success return list of send ids, else return None
        '''
        return DBUtil.exec_query_with_conn(DBUtil.__util_retrieve_chat_send_id, get_id=get_id)


    @staticmethod
    def retrieve_pic_count():
        '''
        get total picture count
        :return: total picture count number if success, -1 if failed
        '''
        return DBUtil.exec_query(DBUtil.__util_retrieve_pic_count)


    @staticmethod
    def retrieve_activity_pics(act_id):
        '''
        retrieve pictures for an activity
        :param act_id: id of an activity
        :return: a list of pic ids
        '''
        k = k_act_pic % act_id
        return DBUtil.__decode_list_with_utf8(rins.smembers(k))


    @staticmethod
    def add_pics_to_activity(act_id, pic_ids):
        '''
        add pictures for an activity
        :param act_id: id of the activity
        :param pic_ids: ids of picture
        :return: added pictures numbers
        '''
        k = k_act_pic % act_id
        return rins.sadd(k, *pic_ids)

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
    def insert_pic_url(pic_url):
        '''
        :param pic_url:
        :return: id of the pic_url if success, None if failed
        '''
        return DBUtil.exec_query(DBUtil.__util_insert_pic_url, url=pic_url)


    @staticmethod
    def insert_new_chat(get_id, send_id, chat_info):
        '''
        insert a record of chat
        :return: True if success, False if failed
        '''
        return DBUtil.exec_query_with_conn(DBUtil.__util_insert_new_chat,
                                           get_id=get_id, send_id=send_id, chat_info=chat_info)


    @staticmethod
    def join_activity(user_id, activity_id_list):
        '''
        :param user_id:
        :param activity_id_list:
        :return: a list of id of activities that failed to joined
        '''
        ss = DBSession()
        failed_list = []
        k = k_user_act % user_id
        for id in activity_id_list:
            if DBUtil.__util_join_activity(ss, user_id, id):
                #add to redis if successfully updated in mysql
                rins.sadd(k, id)
            else:
                failed_list.append(id)
        ss.close()
        return failed_list


    @staticmethod
    def add_user_group(user_id, groups):
        '''
        add an id list of groups to user that the user attentioned
        :param groups: an id list
        :return:  the number of groups that were added, not including the ones that were present
        '''
        num = 0
        k = k_user_group % user_id
        ss = DBSession()
        for gid in groups:
            if rins.sadd(k, gid) is 1 and DBUtil.__util_increase_group_attention(ss, gid):
                num = num + 1
        ss.close()
        return num


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
    def update_userinfo(id, new_info):
        '''
        update user profile by the user id
        :param id: user id
        :param new_info: a dict of new info with keys like:
            [ name, mail, phone, stu_id, college, profession, sex, birthdate, credict, act_v, ava, is_act ]
            NOTE: at least one key is necessary
        :return: a tuple <ok, err>
            'ok': if ok is True, update succeeded, else failed
            'err': if err is not None, error occurred while updating
        '''
        return DBUtil.exec_query(DBUtil.__util_update_userinfo, id=id, info=new_info)


    @staticmethod
    def update_user_avatar(user_id, avatar_id):
        '''
        update user's avatar
        :param user_id: id of user
        :param avatar_id: id of avatar
        :return: True if update success , Flase if failed
        '''
        return DBUtil.exec_query(DBUtil.__util_update_user_avatar, user_id=user_id, avatar_id=avatar_id)


    @staticmethod
    def unfollow_group(user_id, group_id):
        '''
        :param user_id: id of user
        :param group_id: id of group
        :return: True if success, false otherwise
        '''
        k = k_user_group % user_id
        # decrease group attention count
        ss = DBSession()
        DBUtil.__util_increase_group_attention(ss, group_id, -1)
        ss.close()
        return rins.srem(k, group_id) == 1


    @staticmethod
    def remove_user_activities(user_id, activity_ids):
        '''
        remove a list of activties which the user joined
        :param user_id: id of the user
        :param activity_ids: the id list of activities
        :return:  the id list of activities failed to quit
        '''
        ss = DBSession()
        k = k_user_act % user_id
        failed_list = []
        for act_id in activity_ids:
            if DBUtil.__util_delete_joined_user_of_activity(ss, act_id, user_id):
                # if remove the user out of the joined list successfully
                # push updates to redis
                rins.srem(k, act_id)
            else:
                failed_list.append(act_id)
        ss.close()
        return failed_list
