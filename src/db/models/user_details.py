# /src/models/user_details.py

from sqlalchemy import Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func

from db.db import DataBase


class User(DataBase):
    __table__ = Table(
        'user',
        MetaData(),
        Column('id', Integer, primary_key=True),
        Column('server_id', Integer),
        Column('user_id', Integer),
        Column('username', String),
        Column('nickname', String),
        Column('joined_at', DateTime(timezone=True), server_default=func.now())
    )

    def create_user(self, server_id: int, user_id: int, username: str, nickname: str):
        new_user = User(server_id=server_id, user_id=user_id, username=username, nickname=nickname)
        self.session.add(new_user)
        self.session.commit()

    def read_users(self):
        # TODO: do stuff with the data
        users = self.session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Server ID: {user.server_id}, User ID: {user.user_id}, Username: {user.username}, "
                  f"Nickname: {user.nickname}, Joined At: {user.joined_at}")

    def update_user(self, user_id: int, new_nickname: str):
        user_to_update = self.session.query(User).filter_by(user_id=user_id).first()
        if user_to_update:
            user_to_update.nickname = new_nickname
            self.session.commit()

    def destroy_user(self, user_id: int):
        user_to_delete = self.session.query(User).filter_by(user_id=user_id).first()
        if user_to_delete:
            self.session.delete(user_to_delete)
            self.session.commit()

    def close(self):
        self.session.close()

    def create_db_session(self):
        return self.Session()
