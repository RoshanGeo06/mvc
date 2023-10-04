from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    password = Column(String)
    name = Column(String)
    email = Column(String)
    records = relationship('Record', back_populates='user')

class Sample(Base):
    __tablename__ = 'samples'
    sample_id = Column(Integer, primary_key=True)
    sample_name = Column(String)
    description = Column(String)
    age = Column(Integer)
    gender = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    marks = Column(Integer)
    records = relationship('Record', back_populates='sample')

# Define the Records model
class Record(Base):
    __tablename__ = 'records'
    record_id = Column(Integer, primary_key=True)
    details = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    sample_id = Column(Integer, ForeignKey('samples.sample_id'))
    user = relationship('User', back_populates='records')
    sample = relationship('Sample', back_populates='records')
