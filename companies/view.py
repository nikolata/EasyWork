from .controller import CompanyController


class CompanyView:
    def __init__(self):
        self.company = CompanyController()

    def log_in(self):
        email = input("Email: ")
        password = input("Password: ")
        print(self.company.log_in(email=email, password=password))

    def sign_up(self):
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        description = input("Description: ")
        self.company.sign_up(name=name, email=email, password=password, description=description)

    def update_profile(self):
        curr_company = self.company.get_current_company()
        print(curr_company.email)
        print("Old name: " + curr_company.name)
        new_name = input("New name: ")
        print("Old email" + curr_company.email)
        new_email = input("New email: ")
        new_password = input("New password: ")
        print("Old description: " + curr_company.description)
        new_description = input("New description: ")
        self.company.update_profile(name=new_name,
                                    email=new_email,
                                    password=new_password,
                                    description=new_description)

    def show_all_categories(self):
        categories = self.company.get_all_categories()
        for category in categories:
            print(category.category_id, category.name)

    def add_job(self):
        self.show_all_categories()
        category_id = input("Please choose categoy (id): ")
        title = input("Please insert title: ")
        city = input("Please insert city: ")
        position = input("Please insert position: ")
        description = input("Please insert job description: ")
        self.company.add_job(int(category_id), title, city, position, description)

    def show_all_jobs(self):
        jobs = self.company.get_all_jobs()
        for job in jobs:
            # print(job.category.name)
            print(job.title)
            print(job.city)
            print(job.position)
            print(job.description)
            print(job.timestamp)
