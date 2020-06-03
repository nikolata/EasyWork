from .controller import CompanyController
from flask import Flask, render_template, request, redirect, url_for, session
from utls import login_required
from candidates.controller import CandidateController
from settings import app


class CompanyView:
    def __init__(self):
        self.company = CompanyController()

    def log_in(self, email, password):
        return self.company.log_in(email=request.form['email'], password=request.form['password'])

    def change_to_company_home(self):
        return redirect(url_for('company_home'))

    @app.route('/company_home', methods=['POST', 'GET'])
    def company_home():
        if request.method == 'POST':
            if request.form['submit_button'] == 'Add job':
                return redirect(url_for('add_job'))
            if request.form['submit_button'] == 'Show all jobs':
                pass
            if request.form['submit_button'] == 'Delete job':
                pass
            if request.form['submit_button'] == 'Update job':
                pass
        company = CompanyController()
        return render_template("company_home.html", company=company.get_current_company())

    def sign_up(self):
        if request.method == 'POST':
            self.company.sign_up(name=request.form["name"], email=request.form["email"],
                                 password=request.form["password"], description=request.form["description"])
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        return render_template("sign_up.html")

    @login_required
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

    @app.route('/company_home/add_job', methods=['GET', 'POST'])
    def add_job():
        categories = CompanyController().get_all_categories()
        if request.method == 'POST':
            if request.form['salary_type'] == 'lv':
                salary_type = 'lv'
            else:
                salary_type = 'eur'
            if request.form['is_net'] == 'gross':
                is_net = 0
            else:
                is_net = 1
            for category in categories:
                if request.form['category'] == category.name:
                    CompanyController().add_job(int(category.category_id),
                                                request.form['title'],
                                                request.form['city'],
                                                request.form['position'],
                                                request.form['description'],
                                                int(request.form['salary']),
                                                salary_type,
                                                is_net)
                    return redirect(url_for('company_home'))
        return render_template('add_job.html', categories=categories)

    def show_all_jobs(self):
        jobs = self.company.get_all_jobs()
        for job in jobs:
            print('-----------------')
            print(job.job_id)
            print(job.title)
            print(job.city)
            print(job.position)
            print(job.description)
            if job.is_net:
                print(str(job.salary) + job.salary_type + " neto")
            else:
                print(str(job.salary) + job.salary_type + " bruto")
            print(job.timestamp)

    def delete_job(self):
        self.show_all_jobs()
        choosed_job = input("Insert the job id that you want to delete: ")
        self.company.delete_job(choosed_job)

    def update_job(self):
        self.show_all_jobs()
        choosed_job = input("Insert the job id that you want to update: ")
        job = self.company.get_specific_job(choosed_job)
        print("Old title: " + job.title)
        new_title = input("New title: ")
        print("Old city: " + job.city)
        new_city = input("New city: ")
        print("Old position: " + job.position)
        new_position = input("New position: ")
        print("Old description: " + job.description)
        new_description = input("New description: ")
        print("Old salary: " + str(job.salary))
        new_salary = input("New salary: ")
        new_salary_type = input("New salary type: ")
        new_is_net = input("Gross or net [0/1]: ")
        self.company.update_job(choosed_job,
                                new_title,
                                new_city,
                                new_position,
                                new_description,
                                int(new_salary),
                                new_salary_type,
                                int(new_is_net))
