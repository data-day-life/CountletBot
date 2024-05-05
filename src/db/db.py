# /src/db/db.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DataBase:

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.history_table = Table(
            'history',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('user_id', Integer),
            Column('message', String),
            Column('timestamp', DateTime(timezone=True), server_default=func.now())
        )
        self.Base = declarative_base()
        self.Base.metadata.create_all(self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_entry(self, user_id: int, message: str):
        new_entry = History(user_id=user_id, message=message)
        self.session.add(new_entry)
        self.session.commit()

    def read_entries(self):
        entries = self.session.query(History).all()
        for entry in entries:
            print(f"ID: {entry.id}, User ID: {entry.user_id}, Message: {entry.message}, Timestamp: {entry.timestamp}")

    def update_entry(self, user_id: int, new_message: str):
        entry_to_update = self.session.query(History).filter_by(user_id=user_id).first()
        if entry_to_update:
            entry_to_update.message = new_message
            self.session.commit()

    def destroy_entry(self, user_id: int):
        entry_to_delete = self.session.query(History).filter_by(user_id=user_id).first()
        if entry_to_delete:
            self.session.delete(entry_to_delete)
            self.session.commit()

    def close(self):
        self.session.close()

    def create_db_session(self):
        return self.Session()


class History(DataBase):
    __table__ = Table(
        'history',
        MetaData(),
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer),
        Column('message', String),
        Column('timestamp', DateTime(timezone=True), server_default=func.now())
    )
