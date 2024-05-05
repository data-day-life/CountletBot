# /src/db/models/channel_messages.py

from sqlalchemy import Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func

from db.db import DataBase


class ChannelMessages(DataBase):
    __table__ = Table(
        'channel_messages',
        MetaData(),
        Column('id', Integer, primary_key=True),
        Column('channel_id', Integer),
        Column('message_id', Integer),
        Column('message', String),
        Column('timestamp', DateTime(timezone=True), server_default=func.now())
    )

    def create_message(self, channel_id: int, message_id: int, message: str):
        new_message = ChannelMessages(channel_id=channel_id, message_id=message_id, message=message)
        self.session.add(new_message)
        self.session.commit()

    def read_messages(self):
        messages = self.session.query(ChannelMessages).all()
        for message in messages:
            print(f"ID: {message.id}, Channel ID: {message.channel_id}, Message ID: {message.message_id}, Message: {message.message}, Timestamp: {message.timestamp}")

    def update_message(self, message_id: int, new_message: str):
        message_to_update = self.session.query(ChannelMessages).filter_by(message_id=message_id).first()
        if message_to_update:
            message_to_update.message = new_message
            self.session.commit()

    def destroy_message(self, message_id: int):
        message_to_delete = self.session.query(ChannelMessages).filter_by(message_id=message_id).first()
        if message_to_delete:
            self.session.delete(message_to_delete)
            self.session.commit()

    def close(self):
        self.session.close()

    def create_db_session(self):
        return self.Session()
