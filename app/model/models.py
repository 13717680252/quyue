# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TActivity(Base):
    __tablename__ = 't_activity'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    publisher = Column(Integer, nullable=False)
    group_id = Column(Integer, nullable=False)
    description = Column(String(1000), nullable=False)
    create_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    min_num = Column(Integer, nullable=False, server_default=text("'0'"))
    max_num = Column(Integer, nullable=False, server_default=text("'0'"))
    cur_num = Column(Integer, nullable=False, server_default=text("'0'"))
    join_ids = Column(Text, nullable=False)
    is_expired = Column(Integer, nullable=False, server_default=text("'0'"))
    tags = Column(String(1000), nullable=False, server_default=text("''"))
    is_canceled = Column(Integer, nullable=False)
    cancel_date = Column(DateTime)


class TCommentActivity(Base):
    __tablename__ = 't_comment_activity'

    id = Column(BigInteger, primary_key=True)
    activity_id = Column(BigInteger, nullable=False)
    comment_user_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    content = Column(String(100))
    create_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(Integer, nullable=False, server_default=text("'0'"))
    delelte_date = Column(DateTime)


class TCommnetPerson(Base):
    __tablename__ = 't_commnet_people'

    id = Column(BigInteger, primary_key=True)
    activity_id = Column(BigInteger, nullable=False)
    comment_user_id = Column(Integer, nullable=False)
    commented_user_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    content = Column(String(100), nullable=False)
    create_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_date = Column(DateTime)


class TGroup(Base):
    __tablename__ = 't_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    type = Column(Integer, nullable=False, server_default=text("'0'"))
    description = Column(String(1000), nullable=False)
    create_date = Column(Date, nullable=False)
    attention_count = Column(Integer, nullable=False, server_default=text("'0'"))
    activetity_count = Column(Integer, nullable=False, server_default=text("'0'"))


class TUser(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(12), nullable=False)
    password = Column(String(16), nullable=False)
    mail = Column(String(321), nullable=False)
    phone = Column(String(12), nullable=False)
    stu_id = Column(String(16), nullable=False)
    college = Column(String(32), nullable=False)
    profession = Column(String(16), nullable=False)
    sex = Column(String(1), nullable=False)
    birthdate = Column(Date, nullable=False)
    friends = Column(String(1000), nullable=False, server_default=text("''"))
    credit = Column(Integer, nullable=False, server_default=text("'10'"))
    active_value = Column(Integer, nullable=False, server_default=text("'0'"))
    avatar = Column(BigInteger)
    is_activated = Column(String(1), nullable=False, server_default=text("'y'"))
