from .model import JobModel
from database import session_scope


class JobGateway:
    def __init__(self):
        self.job = JobModel

    def add_job(self, category_id, title, city, position, description, company_id):
        with session_scope() as session:
            session.add(JobModel(category_id=category_id,
                                 title=title,
                                 city=city,
                                 position=position,
                                 description=description,
                                 company_id=company_id))

    def get_all_jobs(self, company_id):
        with session_scope() as session:
            return session.query(JobModel).filter(JobModel.company_id.like(company_id)).all()
