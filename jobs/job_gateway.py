from .model import JobModel
from database import session_scope


class JobGateway:
    def __init__(self):
        self.job = JobModel

    def add_job(self, category_id, title, city, position, description, salary, salary_type, is_net, company_id):
        with session_scope() as session:
            session.add(JobModel(category_id=category_id,
                                 title=title,
                                 city=city,
                                 position=position,
                                 description=description,
                                 salary=salary,
                                 salary_type=salary_type,
                                 is_net=is_net,
                                 company_id=company_id))

    def get_all_jobs(self, company_id):
        with session_scope() as session:
            return session.query(JobModel).filter(JobModel.company_id.like(company_id),
                                                  JobModel.available.like(1)).all()

    def delete_job(self, job_id):
        with session_scope() as session:
            session.query(JobModel).filter(JobModel.job_id.like(job_id)).\
                update({JobModel.available: 0}, synchronize_session=False)

    def get_specific_job(self, job_id):
        with session_scope() as session:
            return session.query(JobModel).filter(JobModel.job_id.like(job_id)).first()

    def update_job(self, job_id, title, city, position, description, salary, salary_type, is_net):
        with session_scope() as session:
            session.query(JobModel).filter(JobModel.job_id.like(job_id)).\
                update({JobModel.title: title,
                        JobModel.city: city,
                        JobModel.position: position,
                        JobModel.description: description,
                        JobModel.salary: salary,
                        JobModel.salary_type: salary_type,
                        JobModel.is_net: is_net,
                        }, synchronize_session=False)

    def select_jobs_by_category(category):
        with session_scope() as session:
            return session.query(JobModel).filter(JobModel.category.name == category).all()
