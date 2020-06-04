from .model import MessageModel
from sqlalchemy import and_
from database import session_scope


class MessageGateway:
    def select_messages(company_id, candidate_id):
        with session_scope() as session:
            return session.query(MessageModel).\
                filter(and_(MessageModel.candidate_id == candidate_id,
                            MessageModel.company_id == company_id)).all()

    def add_message(company_id, candidate_id, send_by, message):
        with session_scope() as session:
            session.add(MessageModel(company_id=company_id, candidate_id=candidate_id, send_by=send_by,
                                     message=message))

    def update_seen(self, company_id, candidate_id):
        with session_scope() as session:
            session.query(MessageModel).\
                filter(and_(MessageModel.candidate_id == candidate_id,
                            MessageModel.company_id == company_id)).update({MessageModel.seen: True})

    def select_company_id(self, candidate_id):
        with session_scope() as session:
            return session.query(MessageModel.company).filter(MessageModel.candidate_id == candidate_id).\
                distinct(MessageModel.company_id).all()
