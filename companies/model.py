from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class CompanyModel(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    description = Column(String)
    active = Column(Boolean, default=True)


class ViewedCandidatesByCompany(Base):
    __tablename__ = 'viewed_by_company'
    viewed_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    company = relationship('CompanyModel')


class LikedCandidatesByCompany(Base):
    __tablename__ = 'liked_by_compay'
    liked_id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    timestamp = Column(DateTime, default=datetime.now())
    candidate = relationship('CandidateModel')
    company = relationship('CompanyModel')
