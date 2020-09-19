from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import settings

# engine = create_engine('sqlite:///library.db', echo=True)
engine = create_engine('sqlite:///' + settings.paths.get_campaign_path() + "/campaign_data.db", echo=settings.current['database']['echo'])
Base = declarative_base()

from db import tables


Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

from db import load_db

