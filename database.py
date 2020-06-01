from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///easywork.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
