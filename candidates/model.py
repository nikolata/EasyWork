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
    active = Column(Boolean, default=True)


class ViewedJobsByCandidate(Base):
    __tablename__ = 'viewed_by_candidate'
    viewed_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    job = relationship('JobModel')


class LikedJobsByCandidate(Base):
    __tablename__ = 'liked_by_candidate'
    liked_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    job_id = Column(Integer, ForeignKey('jobs.job_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    job = relationship('JobModel')
