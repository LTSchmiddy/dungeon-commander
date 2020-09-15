from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///library.db', echo=True)
# engine = create_engine('sqlite:///' + settings['database']['location'] + "/library.db")
Base = declarative_base()

from db import tables


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))



