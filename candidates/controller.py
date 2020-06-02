from .gateway import CandidateGateway, ViewedJobsByCandidateGateway, LikedJobsByCandidateGateway
from jobs.job_gateway import JobController
import hashlib


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


class CandidateController:
    def __init__(self):
        self.gateway = CandidateGateway()

    def add_candidate(self, name, email, password, phone, about_me, category_id, cv_link=None):
        password = hash_password(password)
        self.gateway.insert(name, email, password, phone, about_me, cv_link, category_id)

    def activate_account(self, candidate_id):
        self.gateway.update_active(True, candidate_id)

    def deactivate_account(self, candidate_id):
        self.gateway.update_active(False, candidate_id)

    def get_all_jobs_by_category(self, category, candidate_id):
        job_controller = JobController()
        viewed_job_controller = ViewedJobsByCandidateController()
        jobs = job_controller.select_jobs_by_category(category)
        viewed = viewed_job_controller.get_all_jobs(candidate_id)
        result = None
        for job in jobs:
            if job not in viewed:
                result = job
                break
        return result

    def change_profile(self, name, email, password, phone, about_me, cv_link, category_id, candidate_id):
        password = hash_password(password)
        self.gateway.update(name, email, password, phone, about_me, cv_link, category_id, candidate_id)


class ViewedJobsByCandidateController:
    def __init__(self):
        self.gateway = ViewedJobsByCandidateGateway()

    def get_all_jobs(self, candidate_id):
        self.gateway.select_all(candidate_id)


class LikedJobsByCandidateController:
    def __init__(self):
        self.gateway = LikedJobsByCandidateGateway()

    def get_all_jobs(self, candidate_id):
        self.gateway.select_all(candidate_id)
