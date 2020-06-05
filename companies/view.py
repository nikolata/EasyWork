from .controller import CompanyController
from flask import render_template, request, redirect, url_for, session, flash
from utls import login_required
from candidates.controller import CandidateController
from settings import app
from messages.controller import MessageController


class CompanyView:
    def __init__(self):
        self.company = CompanyController()

    def log_in_as_company(self, email, password):
        return self.company.log_in(email=request.form['email'], password=request.form['password'])

    def change_to_company_home(self):
        session['logged_in'] = True
        return redirect(url_for('company_home'))

    @app.route('/company_home', methods=['POST', 'GET'])
    @login_required
    def company_home():
        print(session)
        company = CompanyController()
        candidate = CompanyController().get_unseen_candidates_by_category(session['category'])
        categories = CompanyController().get_all_categories()
        error = None
        if candidate is False:
            error = 'No more candidates of this category'
        if request.method == 'POST':
            if request.form['submit_button'] == 'Manage jobs':
                return redirect(url_for('manage_jobs'))
            if request.form['submit_button'] == 'Profile settings':
                return redirect(url_for('profile_settings'))
            if request.form['submit_button'] == 'Log out':
                return redirect(url_for('logout'))
            if request.form['submit_button'] == 'Pass':
                company.view_candidate(candidate.candidate_id)
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Like':
                company.view_candidate(candidate.candidate_id)
                company.like_candidate(candidate.candidate_id)
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Change category':
                session['category'] = int(request.form['category'])
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Liked candidates':
                return redirect(url_for('liked_candidates'))
            if request.form['submit_button'] == 'Liked jobs':
                return redirect(url_for('liked_jobs'))
            # if request.form['submit_button'] == 'Delete job':
            #     pass
            # if request.form['submit_button'] == 'Update job':
            #     pass
        return render_template("company_home.html", company=company.get_current_company(), candidate=candidate,
                               error=error, categories=categories)

    def sign_up(self):
        if request.method == 'POST':
            self.company.sign_up(name=request.form["name"], email=request.form["email"],
                                 password=request.form["password"], description=request.form["description"])
            session['logged_in'] = True
            return redirect(url_for('welcome'))
        return render_template("sign_up_as_company.html")

    @app.route('/logout')
    @login_required
    def logout():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('welcome'))

    @app.route('/company_home/liked_candidates', methods=['POST', 'GET'])
    @login_required
    def liked_jobs():
        liked = CompanyController().get_candidates_that_liked_company_jobs()
        error = None
        candidates = CompanyController().get_liked_candidates_by_company()
        categories = CompanyController().get_all_categories()
        if len(liked) == 0:
            error = 'Still 0 likes for your job :<'
        if request.method == 'POST':
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Send message':
                pass
        return render_template('liked_job_from_candidates.html', candidates=candidates, error=error, liked=liked,
                               categories=categories)

    @app.route('/company_home/liked_candidates', methods=['POST', 'GET'])
    @login_required
    def liked_candidates():
        candidates = CompanyController().get_liked_candidates_by_company()
        categories = CompanyController().get_all_categories()
        error = None
        if len(candidates) == 0:
            error = 'You dont have liked candidates'
        if request.method == 'POST':
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Delete':
                CompanyController().delete_liked_candidade(int(request.form['candidate']))
                return redirect(url_for('liked_candidates'))
            if request.form['submit_button'] == 'Send message':
                pass
        return render_template('liked_candidates.html', candidates=candidates, error=error,
                               categories=categories)

    @app.route('/company_home/profile_settings', methods=['POST', 'GET'])
    @login_required
    def profile_settings():
        company = CompanyController().get_current_company()
        if request.method == 'POST':
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('company_home'))
            if request.form['submit_button'] == 'Update profile':
                return redirect(url_for('update_profile'))
            if request.form['submit_button'] == 'Change password':
                return redirect(url_for('change_password'))
            if request.form['submit_button'] == 'Delete profile':
                CompanyController().delete_account(company.company_id)
                return redirect(url_for('welcome'))
        return render_template('profile_settings.html', company=company)

    @app.route('/company_home/manage_jobs', methods=['POST', 'GET'])
    @login_required
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

    @app.route('/company_home/manage_jobs/update_profile', methods=['POST', 'GET'])
    @login_required
    def update_profile():
        curr_company = CompanyController().get_current_company()

        if request.method == 'POST':
            if request.form['submit_button'] == 'Update':
                CompanyController().update_profile(name=request.form['company_name'],
                                                   email=request.form['company_email'],
                                                   password=curr_company.password,
                                                   description=request.form['company_description'])
                return redirect(url_for('profile_settings'))
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('profile_settings'))
        return render_template('update_company_profile.html', company=curr_company)

    @app.route('/company_home/manage_jobs/change_password', methods=['POST', 'GET'])
    @login_required
    def change_password():
        error = None
        if request.method == 'POST':
            if request.form['submit_button'] == 'Change':
                if request.form['first_new_password'] != request.form['second_new_password']:
                    error = 'New passwords are not the same'
                elif CompanyController().change_password(request.form['old_password'],
                                                         request.form['first_new_password']) is False:
                    error = 'Wrong old password'
                else:
                    return redirect(url_for('profile_settings'))
            if request.form['submit_button'] == 'Go back':
                return redirect(url_for('profile_settings'))
        return render_template('change_company_password.html', error=error)

    def show_all_categories(self):
        categories = self.company.get_all_categories()
        for category in categories:
            print(category.category_id, category.name)

    @app.route('/company_home/add_job', methods=['GET', 'POST'])
    @login_required
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
    @login_required
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

    @app.route("/company_home/chats_company", methods=["POST"])
    @login_required
    def show_chats_company():
        curr_company = CompanyController().get_current_company()
        message = MessageController()
        messages = message.get_all_messages_with_given_company_and_candidate(curr_company.id,
                                                                             int(request.form["candidate"]))
        return render_template("messages.html", messages=messages)
