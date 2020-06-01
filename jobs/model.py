from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class CategoryModel(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class JobModel(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    title = Column(String)
    city = Column(String)
    position = Column(String)
    description = Column(String)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    timestamp = Column(DateTime, default=datetime.now())
    category = relationship('CategoryModel')
    company = relationship('CompanyModel')
