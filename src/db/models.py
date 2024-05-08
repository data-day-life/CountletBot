# /src/db/models/models.py

from sqlalchemy import Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func

from db.db import DataBase


class CountChannels(DataBase):
    __table__ = Table(
        'count_channels',
        MetaData(),
        Column('channel_id', Integer),
        Column('server_id', Integer),
        Column('channel_name', String),
        Column('start_after_msg_id', Integer),
        Column('timestamp', DateTime(timezone=True), server_default=func.now())
    )


class ChannelMessages(DataBase):
       __table__ = Table(
           'channel_messages',
           MetaData(),
           Column('message_id', Integer),
           Column('channel_id', Integer),
           Column('user_id', Integer),
           Column('message', String),
           Column('timestamp', DateTime(timezone=True), server_default=func.now())
       )


class Servers(DataBase):
    __table__ = Table(
        'servers',
        MetaData(),
        Column('server_id', Integer),
        Column('server_name', String),
        Column('timestamp', DateTime(timezone=True), server_default=func.now())
    )

