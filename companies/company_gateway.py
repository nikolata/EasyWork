from .model import CompanyModel, ViewedCandidatesByCompanyModel, LikedCandidatesByCompanyModel
from candidates.model import CandidateModel, LikedJobsByCandidateModel
from messages.model import MessageModel
from database import session_scope


class CompanyGateway:

    def log_in(self, email, password):
        with session_scope() as session:
            return session.query(CompanyModel).filter(CompanyModel.email.like(email),
                                                      CompanyModel.password.like(password),
                                                      CompanyModel.active.like(1)).all()

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

    def get_unseen_candidates_of_category(self, category_id):
        with session_scope() as session:
            return session.query(ViewedCandidatesByCompanyModel.candidate_id).join(CandidateModel).\
                filter(CandidateModel.field_of_work.like(category_id)).all()

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

    def change_password(self, new_password, company_id):
        with session_scope() as session:
            session.query(CompanyModel).filter(CompanyModel.company_id.like(company_id)).\
                update({CompanyModel.password: new_password}, synchronize_session=False)

    def make_unactive_account(self, company_id):
        with session_scope() as session:
            session.query(CompanyModel).filter(CompanyModel.company_id.like(company_id)).\
                update({CompanyModel.active: 0}, synchronize_session=False)

    def get_all_clients_by_category(self, category_id):
        with session_scope() as session:
            return session.query(CandidateModel).filter(CandidateModel.field_of_work.like(category_id)).all()

    def get_all_seen_candidates(self, company_id):
        with session_scope() as session:
            return session.query(ViewedCandidatesByCompanyModel).\
                filter(ViewedCandidatesByCompanyModel.company_id.like(company_id)).all()

    def view_candidate(self, candidate_id, company_id):
        with session_scope() as session:
            session.add(ViewedCandidatesByCompanyModel(candidate_id=candidate_id, company_id=company_id))

    def like_candidate(self, candidate_id, company_id):
        with session_scope() as session:
            session.add(LikedCandidatesByCompanyModel(candidate_id=candidate_id, company_id=company_id))

    def delete_liked_candidate(self, candidate_id, company_id):
        with session_scope() as session:
            liked = session.query(LikedCandidatesByCompanyModel).\
                filter(LikedCandidatesByCompanyModel.candidate_id.like(candidate_id),
                       LikedCandidatesByCompanyModel.company_id.like(company_id)).first()
            session.delete(liked)

    def get_candidate_who_liked_this_job(self, job_id):
        with session_scope() as session:
            return session.query(LikedJobsByCandidateModel).\
                filter(LikedJobsByCandidateModel.job_id.like(job_id)).first()

    def get_all_candidates(self):
        with session_scope() as session:
            return session.query(CandidateModel).all()
