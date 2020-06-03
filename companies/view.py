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
            if request.form['submit_button'] == 'Manage jobs':
                return redirect(url_for('manage_jobs'))
            # if request.form['submit_button'] == 'Show all jobs':
            #     pass
            # if request.form['submit_button'] == 'Delete job':
            #     pass
            # if request.form['submit_button'] == 'Update job':
            #     pass
        company = CompanyController()
        return render_template("company_home.html", company=company.get_current_company())

    def sign_up(self):
        if request.method == 'POST':
            self.company.sign_up(name=request.form["name"], email=request.form["email"],
                                 password=request.form["password"], description=request.form["description"])
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        return render_template("sign_up.html")

    @app.route('/company_home/manage_jobs', methods=['POST', 'GET'])
    def manage_jobs():
        jobs = CompanyController().get_all_jobs()
        categories = CompanyController().get_all_categories()
        if request.method == 'POST':
            if request.form['submit_button'] == 'Add job':
                return redirect(url_for('add_job'))
            if request.form['submit_button'] == 'Update job':
                session['job_id'] = request.form['job']
                return redirect(url_for('update_job'))
            if request.form['submit_button'] == 'Delete job':
                CompanyController().delete_job(int(request.form['job']))
                return redirect(url_for('manage_jobs'))
        return render_template('manage_jobs.html', jobs=jobs, categories=categories)

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
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('company_home'))
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
                    return redirect(url_for('manage_jobs'))
        return render_template('add_job.html', categories=categories)

    # def show_all_jobs(self):
    #     return self.company.get_all_jobs()

    @app.route('/company_home/update_job', methods=['GET', 'POST'])
    def update_job():
        jobs = CompanyController().get_all_jobs()
        for job in jobs:
            if job.job_id == int(session['job_id']):
                current_job = job
        if request.method == 'POST':
            if request.form['submit_button'] == 'Update job':
                if request.form['job_salary_type'] == 'lv':
                    salary_type = 'lv'
                else:
                    salary_type = 'eur'
                if request.form['is_net'] == 'gross':
                    is_net = 0
                else:
                    is_net = 1
                CompanyController().update_job(current_job.job_id,
                                               request.form['job_title'],
                                               request.form['job_city'],
                                               request.form['job_position'],
                                               request.form['job_description'],
                                               int(request.form['job_salary']),
                                               salary_type,
                                               is_net)
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('company_home'))
        return render_template('update_job.html', job=current_job)
