from .model import CompanyModel
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
