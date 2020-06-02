from .company_gateway import CompanyGateway
from jobs.controller import CategoryController, JobController
from utls import hash_password
import settings


class CompanyController:
    def __init__(self):
        self.company_gateway = CompanyGateway()

    def log_in(self, email, password):
        password = hash_password(password)
        company = self.company_gateway.log_in(email=email, password=password)
        if len(company) != 0:
            settings.CURRENT_COMPANY_EMAIL = email
            return company
        else:
            return False

    def sign_up(self, name, email, password, description):
        password = hash_password(password)
        self.company_gateway.sign_up(name=name, email=email, password=password, description=description)
        settings.CURRENT_COMPANY_EMAIL = email

    def get_current_company(self):
        return self.company_gateway.get_current_company(settings.CURRENT_COMPANY_EMAIL)

    def update_profile(self, name, email, password, description):
        return self.company_gateway.update_profile(name=name,
                                                   email=email,
                                                   password=hash_password(password),
                                                   description=description,
                                                   current=settings.CURRENT_COMPANY_EMAIL)

    def get_all_categories(self):
        category = CategoryController()
        return category.get_all_categories()

    def add_job(self, category_id, title, city, position, description, salary, salary_type, is_net):
        company = self.get_current_company()
        job = JobController()
        return job.add_job(category_id, title, city, position, description, salary, salary_type, is_net,
                           int(company.company_id))

    def get_all_jobs(self):
        company = self.get_current_company()
        job = JobController()
        return job.get_all_jobs(int(company.company_id))

    def delete_job(self, job_id):
        job = JobController()
        job.delete_job(job_id)

    def get_specific_job(self, job_id):
        job = JobController()
        return job.get_specific_job(job_id)

    def update_job(self, job_id, title, city, position, description, salary, salary_type, is_net):
        job = JobController()
        job.update_job(job_id, title, city, position, description, salary, salary_type, is_net)

    def get_max_id_from_viewed_candidates_and_category(self, category_id):
        company = self.get_current_company()
        max_id = self.company_gateway.get_max_id_from_viewed_candidates_and_category(category_id,
                                                                                     company.company_id)
        return int(max_id[0])

    def get_unseen_candidates_of_category(self, category_id):
        max_id = self.get_max_id_from_viewed_candidates_and_category(category_id)
        return self.company_gateway.get_unseen_candidates_of_category(max_id, category_id)

    def get_liked_candidates_by_company(self):
        company = self.get_current_company()
        return self.company_gateway.get_liked_candidates_by_company(company.company_id)

    def get_all_candidates_that_liked_companys_job(self, job_id):
        return self.company_gateway.get_all_candidates_that_liked_companys_job(job_id)

    def write_message_to_candidate(self, candidate_id, message):
        company = self.get_current_company()
        self.company_gateway.write_message_to_candidate(candidate_id, company.company_id, message)

    def get_all_messages_with_candidate(self, candidate_id):
        company = self.get_current_company()
        return self.company_gateway.get_all_messages_with_candidate(candidate_id, company.company_id)
