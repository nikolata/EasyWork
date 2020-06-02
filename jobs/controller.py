from .category_gateway import CategoryGateway
from .job_gateway import JobGateway


class CategoryController:
    def __init__(self):
        self.category_gateway = CategoryGateway()

    def get_all_categories(self):
        return self.category_gateway.get_all_categories()


class JobController:
    def __init__(self):
        self.job_gateway = JobGateway()

    def add_job(self, category_id, title, city, position, description, company_id):
        self.job_gateway.add_job(category_id, title, city, position, description, company_id)

    def get_all_jobs(self, company_id):
        return self.job_gateway.get_all_jobs(company_id)
