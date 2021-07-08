import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Account(Base):
#     __tablename__ = 'account'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     login = Column(String)
#     password = Column(String, unique=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login = Column(String)
    name = Column(String)
    creation_date = Column(DateTime, default=datetime.datetime.now())


# class UserGroupRelation(Base):
#     __tablename__ = 'user_group_relation'
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(Integer, ForeignKey('user.id'))

