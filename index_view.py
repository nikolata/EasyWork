from companies.view import CompanyView


class CompanyCaller:
    def __init__(self):
        self.company = CompanyView()

    def call_sign_up(self):
        self.company.sign_up()

    def call_log_in(self):
        self.company.log_in()

    def call_update_profile(self):
        self.company.update_profile()

    def call_show_all_categories(self):
        self.company.show_all_categories()

    def call_add_job(self):
        self.company.add_job()

    def call_show_all_jobs(self):
        self.company.show_all_jobs()