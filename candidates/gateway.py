from .model import CandidateModel, ViewedJobsByCandidateModel
from database import session_scope
from sqlalchemy import and_


class CandidateGateway:
    def insert(self, name, email, password, phone, about_me, cv_link, category_id):
        with session_scope() as session:
            session.add(CandidateModel(name=name, email=email, password=password,
                                       phone=phone, about_me=about_me, cv_link=cv_link, field_of_work=category_id))

    def update_active(self, active, candidate_id):
        with session_scope() as session:
            session.query(CandidateModel).filter(CandidateModel.candidate_id == candidate_id).\
                update({CandidateModel.active: active})

    def update(self, name, email, password, phone, about_me, cv_link, category_id, candidate_id):
        with session_scope() as session:
            candidate = session.query(CandidateModel).filter(CandidateModel.candidate_id == candidate_id).first()
            candidate.name = name
            candidate.email = email
            candidate.password = password
            candidate.phone = phone
            candidate.about_me = about_me
            candidate.cv_link = cv_link
            candidate.category_id = category_id

    def select_one(self, email, password):
        with session_scope() as session:
            return session.query(CandidateModel).\
                filter(and_(CandidateModel.email == email, CandidateModel.password == password)).first()


class ViewedJobsByCandidateGateway:
    def select_all(self, candidate_id):
        with session_scope() as session:
            return session.query(ViewedJobsByCandidateModel).\
                filter(ViewedJobsByCandidateModel.candidate_id == candidate_id).all()


class LikedJobsByCandidateGateway:
    def select_all(self, candidate_id):
        with session_scope() as session:
            return session.query(ViewedJobsByCandidateModel).\
                filter(ViewedJobsByCandidateModel.candidate_id == candidate_id).all()
