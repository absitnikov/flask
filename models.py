from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import atexit

engine = create_engine('postgresql://app:1234@127.0.0.1:5431/app')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Ads(Base):
    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=50), nullable=False)
    description = Column(String(length=250))
    creation_date = Column(DateTime, server_default=func.now())
    owner_id = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


class HttpError(Exception):

    def __init__(self, status_code: int, message: str | dict | list):
        self.status_code = status_code
        self.message = message
