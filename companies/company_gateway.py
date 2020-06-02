from .model import CompanyModel, ViewedCandidatesByCompanyModel, LikedCandidatesByCompanyModel
from candidates.model import CandidateModel, LikedJobsByCandidateModel
from messages.model import MessageModel
from database import session_scope


class CompanyGateway:

    def log_in(self, email, password):
        with session_scope() as session:
            return session.query(CompanyModel).filter(CompanyModel.email.like(email),
                                                      CompanyModel.password.like(password)).all()

    def sign_up(self, name, email, password, description):
        with session_scope() as session:
            session.add(CompanyModel(name=name, email=email, password=password, description=description))

    def get_current_company(self, company_email):
        with session_scope() as session:
            return session.query(CompanyModel).filter(CompanyModel.email.like(company_email)).first()

    def update_profile(self, name, email, password, description, current):
        with session_scope() as session:
            session.query(CompanyModel).filter(CompanyModel.email.like(current)).\
                update({CompanyModel.name: name, CompanyModel.email: email,
                        CompanyModel.password: password,
                        CompanyModel.description: description}, synchronize_session=False)

    def get_max_id_from_viewed_candidates_and_category(self, category_id, company_id):
        with session_scope() as session:
            return session.query(ViewedCandidatesByCompanyModel.candidate_id).join(CandidateModel).\
                filter(ViewedCandidatesByCompanyModel.company_id.like(company_id),
                       CandidateModel.field_of_work.like(category_id)).\
                order_by(ViewedCandidatesByCompanyModel.viewed_id.desc()).first()

    def get_unseen_candidates_of_category(max_id, category_id):
        with session_scope() as session:
            return session.query(ViewedCandidatesByCompanyModel.candidate_id).join(CandidateModel).\
                filter(ViewedCandidatesByCompanyModel.candidate_id > max_id,
                       CandidateModel.field_of_work.like(category_id)).all()

    def get_liked_candidates_by_company(self, company_id):
        with session_scope() as session:
            return session.query(CandidateModel).join(LikedCandidatesByCompanyModel).\
                filter(LikedCandidatesByCompanyModel.company_id.like(company_id)).all()

    def get_all_candidates_that_liked_companys_job(self, job_id):
        with session_scope() as session:
            return session.query(CandidateModel).join(LikedJobsByCandidateModel).\
                filter(LikedJobsByCandidateModel.job_id.like(job_id)).all()

    def write_message_to_candidate(self, candidate_id, company_id, message):
        with session_scope() as session:
            session.add(MessageModel(company_id=company_id,
                                     candidate_id=candidate_id,
                                     send_by=0,
                                     seen=0,
                                     message=message))

    def get_all_messages_with_candidate(self, candidate_id, company_id):
        with session_scope() as session:
            session.query(MessageModel).filter(MessageModel.candidate_id.like(candidate_id),
                                               MessageModel.company_id.like(company_id)).all()
            session.query(MessageModel).filter(MessageModel.candidate_id.like(candidate_id),
                                               MessageModel.company_id.like(company_id)).\
                update({MessageModel.seen: 1}, synchronize_session=False)
