from .company_gateway import CompanyGateway
from jobs.controller import CategoryController, JobController
from .utls import hash_password
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

    def add_job(self, category_id, title, city, position, description):
        company = self.get_current_company()
        job = JobController()
        return job.add_job(category_id, title, city, position, description, int(company.company_id))

    def get_all_jobs(self):
        company = self.get_current_company()
        job = JobController()
        return job.get_all_jobs(int(company.company_id))
