# /src/db/db.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DataBase:

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.Base = declarative_base()
        self.Base.metadata.create_all(self.engine, checkfirst=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_table(self, table_properties: dict):
        table = Table(
            table_properties['table_name'],
            self.metadata
        )

    def create_entry(self, server_id: int, server_name: str):
        new_entry = Servers(server_id=server_id, server_name=server_name)
        self.session.add(new_entry)
        self.session.commit()

    def read_entries(self):
        # TODO: do stuff with the entries
        entries = self.session.query(Servers).all()
        for entry in entries:
            print(f"server_id: {entry.server_id}, server_name: {entry.server_name},  Timestamp: {entry.timestamp}")

    def update_entry(self, server_id: int, server_name: str):
        entry_to_update = self.session.query(Servers).filter_by(server_id=server_id).first()
        if entry_to_update:
            entry_to_update.message = server_name
            self.session.commit()

    def destroy_entry(self, server_id: int):
        entry_to_delete = self.session.query(Servers).filter_by(server_id=server_id).first()
        if entry_to_delete:
            self.session.delete(entry_to_delete)
            self.session.commit()

    def close(self):
        self.session.close()

    def create_db_session(self):
        return self.Session()


