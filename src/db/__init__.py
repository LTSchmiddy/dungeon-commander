from sqlalchemy import *
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import settings


# engine = create_engine('sqlite:///library.db', echo=True)

Base = declarative_base()

from db import tables
from db import load_db

db_engine: Engine = None
Session = None

def init():
    global Session, db_engine
    db_engine = create_engine('sqlite:///' + settings.paths.get_campaign_path() + "/campaign_data.db", echo=settings.current['database']['echo'])
    Base.metadata.create_all(db_engine)
    Session = scoped_session(sessionmaker(bind=db_engine))



