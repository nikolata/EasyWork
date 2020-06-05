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
            return True
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
                                                   password=password,
                                                   description=description,
                                                   current=settings.CURRENT_COMPANY_EMAIL)

    def delete_account(self, company_id):
        return self.company_gateway.make_unactive_account(company_id)

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

    def change_password(self, old_password, new_password):
        company = self.get_current_company()
        old_password = hash_password(old_password)
        if old_password != company.password:
            return False
        self.company_gateway.change_password(hash_password(new_password), company.company_id)
        return True

    def update_job(self, job_id, title, city, position, description, salary, salary_type, is_net):
        job = JobController()
        job.update_job(job_id, title, city, position, description, salary, salary_type, is_net)

    # def get_max_id_from_viewed_candidates_and_category(self, category_id):
    #     company = self.get_current_company()
    #     max_id = self.company_gateway.get_max_id_from_viewed_candidates_and_category(category_id,
    #                                                                                  company.company_id)
    #     if max_id is None:
    #         return 0
    #     else:
    #         return int(max_id[0])

    # def give_one_candidate(self, category_id):
    #     candidates = self.get_unseen_candidates_of_category(category_id)
    #     for candidate in candidates:
    #         yield candidate

    # def get_unseen_candidates_of_category(self, category_id):
    #     max_id = self.get_max_id_from_viewed_candidates_and_category(category_id)
    #     return self.company_gateway.get_unseen_candidates_of_category(max_id, category_id)
    def get_candidates_by_category(self, category_id):
        return self.company_gateway.get_all_clients_by_category(category_id)

    def get_unseen_candidates_by_category(self, category_id):
        candidates = self.get_candidates_by_category(category_id)
        company = self.get_current_company()
        print(candidates)
        seen_candidates = self.company_gateway.get_all_seen_candidates(company.company_id)
        print(seen_candidates)
        if len(seen_candidates) == 0 and len(candidates) != 0:
            return candidates[0]
        for candidate in candidates:
            not_seen = True
            for seen_candidate in seen_candidates:
                if candidate.candidate_id == seen_candidate.candidate_id:
                    not_seen = False
            if not_seen:
                return candidate
        return False

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

    def view_candidate(self, candidate_id):
        company = self.get_current_company()
        self.company_gateway.view_candidate(candidate_id, company.company_id)

    def like_candidate(self, candidate_id):
        company = self.get_current_company()
        self.company_gateway.like_candidate(candidate_id, company.company_id)

    def delete_liked_candidade(self, candidate_id):
        company = self.get_current_company()
        self.company_gateway.delete_liked_candidate(candidate_id, company.company_id)

    def get_candidates_that_liked_company_jobs(self):
        jobs = self.get_all_jobs()
        all_liked = []
        for job in jobs:
            liked = self.company_gateway.get_candidate_who_liked_this_job(job.job_id)
            if liked is not None:
                all_liked.append(liked)
        return all_liked

    def get_all_candidates(self):
        return self.company_gateway.get_all_candidates()
