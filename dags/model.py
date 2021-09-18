import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Date


class Connection(object):

    def __init__(self, db_connection):
        engine = create_engine(db_connection)
        self.engine = engine

    def get_session(self):
        Session = sessionmaker(bind=self.engine)

        return Session()

    def get_engine(self):
        return self.engine


Base = declarative_base()


def init_db(db_connection):
    engine = create_engine(db_connection)
    Base.metadata.create_all(bind=engine)

class Tomtom(Base):
    __tablename__ = 'tomtom'
    
    timestamp = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    traffic_index = Column(Integer)
    jams_count = Column(Integer)
    jams_length = Column(Float)
    jams_delay = Column(Float)
    traffic_index_weekago = Column(Integer)
    weekday = Column(String)

    def __init__(self, timestamp, date_time, traffic_index, jams_count, jams_length, jams_delay, traffic_index_weekago, weekday):
        self.timestamp = timestamp
        self.date_time = date_time
        self.traffic_index = traffic_index
        self.jams_count = jams_count
        self.jams_length = jams_length
        self.jams_delay = jams_delay
        self.traffic_index_weekago = traffic_index_weekago
        self.weekday = weekday