from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class MessageModel(Base):
    __tablename__ = 'messages'
    message_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    candidate_id = Column(Integer, ForeignKey('candidates.candidate_id'))
    timestamp = Column(DateTime, default=datetime.now())
    send_by = Column(Boolean)
    seen = Column(Boolean, default=False)
    message = Column(String)
    company = relationship('CompanyModel', lazy="joined")
    candidate = relationship('CandidateModel', lazy="joined")
