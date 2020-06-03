from .controller import CandidateController, ViewedJobsByCandidateController, LikedJobsByCandidateController
from flask import render_template, request, redirect, url_for, session
from utls import login_required
from settings import app
from jobs.controller import CategoryController


class CandidateView:
    def __init__(self):
        self.controller = CandidateController()

    def sign_up(self):
        error = None
        category = CategoryController()
        categories = category.get_all_categories()
        print(categories)
        if request.method == 'POST':
            print(request.form["category"])
            if request.form["first_name"] == "" or request.form["last_name"] == "" or\
                    request.form["password"] == "" or request.form["category"] == "":
                error = "Invalid input"
            else:
                name = request.form["first_name"] + " " + request.form["last_name"]
                self.controller.sign_up(name=name, email=request.form["email"], password=request.form["password"],
                                        category=request.form["category"], phone=request.form["phone"],
                                        about_me=request.form["about_me"], cv_link=request.form["cv_link"])
                session['logged_in'] = True
                return redirect(url_for('welcome'))
        return render_template("sign_up_as_candidate.html", error=error, categories=categories)

    def log_in(self, email, password):
        candidate = self.controller.log_in(email, password)
        if candidate:
            session["candidate_id"] = candidate.candidate_id
        return candidate

    @app.route('/log_out')
    def log_out():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect('/')

    def change_to_candidate_home(self):
        return redirect(url_for('candidate_home'))

    @login_required
    @staticmethod
    @app.route('/candidate_home', methods=['POST', 'GET'])
    def candidate_home():
        category = CategoryController()
        categories = category.get_all_categories()
        return render_template("candidate_home.html", categories=categories)

    @app.route('/candidate_home/edit')
    def edit_profile():
        return "Edit"

    @login_required
    @app.route("/candidate_home/chats")
    def show_chats():
        return "Chats"

    @login_required
    @app.route("/candidate_home/viewed")
    def show_viewed_jobs():
        controller = ViewedJobsByCandidateController()
        jobs = controller.get_all_jobs(session["candidate_id"])
        return render_template("all_jobs.html", jobs=jobs, viewed_liked="Viewed")

    @login_required
    @app.route("/candidate_home/liked")
    def show_liked_jobs():
        controller = LikedJobsByCandidateController()
        jobs = controller.get_all_jobs(session["candidate_id"])
        return render_template("all_jobs.html", jobs=jobs, viewed_liked="Liked")
