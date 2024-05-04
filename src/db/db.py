# /src/db/db.py
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection string
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
engine = create_engine(DATABASE_URL)

# Define the table
metadata = MetaData()
history_table = Table(
    'history',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer),
    Column('message', String),
    Column('timestamp', DateTime(timezone=True), server_default=func.now())
)

# Create a declarative base
Base = declarative_base()

# Define a model class for the 'history' table
class History(Base):
    __table__ = history_table

# Create the table if it doesn't exist
Base.metadata.create_all(engine, checkfirst=True)

# Create, read, update, and destroy entries in the database using SQLAlchemy ORM
Session = sessionmaker(bind=engine)
session = Session()

# Example of creating an entry
new_entry = History(user_id=1, message='Hello, world!')
session.add(new_entry)
session.commit()

# Example of reading entries
entries = session.query(History).all()
for entry in entries:
    print(f"ID: {entry.id}, User ID: {entry.user_id}, Message: {entry.message}, Timestamp: {entry.timestamp}")

# Example of updating an entry
entry_to_update = session.query(History).filter_by(user_id=1).first()
if entry_to_update:
    entry_to_update.message = 'Updated message'
    session.commit()

# Example of destroying (deleting) an entry
entry_to_delete = session.query(History).filter_by(user_id=1).first()
if entry_to_delete:
    session.delete(entry_to_delete)
    session.commit()