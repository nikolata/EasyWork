from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class CandidateModel(Base):
    __tablename__ = 'candidates'
    candidate_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String)
    about_me = Column(String)
    cv_link = Column(String)
    field_of_work = Column(Integer, ForeignKey('categories.category_id'))
    active = Column(Boolean, default=True)
    category = relationship('CategoryModel')


class ViewedJobsByCandidateModel(Base):
    __tablename__ = 'viewed_by_candidate'
    viewed_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    job = relationship('JobModel', lazy="joined")

    def __str__(self):
        return f'''Viewed at: {self.timestamp}\n
                   {self.job}'''


class LikedJobsByCandidateModel(Base):
    __tablename__ = 'liked_by_candidate'
    liked_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    job = relationship('JobModel', lazy="joined")

    def __str__(self):
        return f'''Viewed at: {self.timestamp}\n
                   {self.job}'''
