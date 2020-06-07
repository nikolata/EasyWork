from .controller import CandidateController, ViewedJobsByCandidateController, LikedJobsByCandidateController
from flask import render_template, request, redirect, url_for, session
from utls import login_required
from settings import app
from jobs.controller import CategoryController
from messages.controller import MessageController


class CandidateView:
    def __init__(self):
        self.controller = CandidateController()

    def sign_up(self):
        error = None
        category = CategoryController()
        categories = category.get_all_categories()
        if request.method == 'POST':
            print(request.form["category"])
            if request.form["first_name"] == "" or request.form["last_name"] == "" or\
                    request.form["password"] == "" or request.form["category"] == "":
                error = "Missing fields"
            else:
                name = request.form["first_name"] + " " + request.form["last_name"]
                self.controller.sign_up(name=name, email=request.form["email"], password=request.form["password"],
                                        category_id=request.form["category"], phone=request.form["phone"],
                                        about_me=request.form["about_me"], cv_link=request.form["cv_link"])
                session['logged_in'] = True
                return redirect(url_for('welcome'))
        return render_template("sign_up_as_candidate.html", error=error, categories=categories)

    def log_in(self, email, password):
        candidate = self.controller.log_in(email, password)
        if candidate:
            session["candidate_id"] = candidate.candidate_id
            session["password"] = password
        return candidate

    @app.route('/log_out')
    @login_required
    def log_out():
        session.pop('logged_in', None)
        session.pop('candidate_id', None)
        return redirect('/')

    def change_to_candidate_home(self):
        session['logged_in'] = True
        return redirect(url_for('candidate_home'))

    @app.route('/candidate_home', methods=['POST', 'GET'])
    @login_required
    def candidate_home():
        category = CategoryController()
        categories = category.get_all_categories()
        message = MessageController()
        messages = message.get_all_companies_a_candidate_messaged(session["candidate_id"])
        companies = [message.company for message in messages]
        print(companies)
        return render_template("candidate_home.html", categories=categories,companies=companies)

    
    @app.route('/candidate_home/edit')
    @login_required
    def edit_profile():
        controller = CandidateController()
        candidate = controller.get_candidate(session['candidate_id'])
        candidate_name = candidate.name.split()
        first_name = candidate_name[0]
        last_name = candidate_name[1]
        category = CategoryController()
        categories = category.get_all_categories()
        return render_template("candidate_profile.html", candidate=candidate,
                               first_name=first_name, last_name=last_name, categories=categories)

    
    @app.route("/candidate_home/edited", methods=["POST"])
    @login_required
    def update_candidate_profile():
        error = None
        category = CategoryController()
        categories = category.get_all_categories()
        controller = CandidateController()
        candidate = controller.get_candidate(session['candidate_id'])
        candidate_name = candidate.name.split()
        first_name = candidate_name[0]
        last_name = candidate_name[1]
        password = session["password"]
        if request.method == 'POST':
            print(request.form["category"])
            if request.form["first_name"] == "" or request.form["last_name"] == "" or\
                    request.form["old_password"] == "" or request.form["category"] == "":
                error = "Missing fields"
                return render_template("candidate_profile.html", candidate=candidate, first_name=first_name,
                                       last_name=last_name, categories=categories, error=error)
            if request.form["old_password"] != session["password"]:
                error = "Wrong old password"
                return render_template("candidate_profile.html", candidate=candidate, first_name=first_name,
                                       last_name=last_name, categories=categories, error=error)
            elif request.form["new_password"] != request.form["new_again_password"]:
                error = "Wrong new password"
                return render_template("candidate_profile.html", candidate=candidate, first_name=first_name,
                                       last_name=last_name, categories=categories, error=error)
            elif request.form["new_password"] != "":
                password = request.form["new_password"]
            else:
                name = request.form["first_name"] + " " + request.form["last_name"]
                controller.change_profile(session["candidate_id"], name=name, email=request.form["email"],
                                          password=password,
                                          category_id=request.form["category"], phone=request.form["phone"],
                                          about_me=request.form["about_me"], cv_link=request.form["cv_link"])
                session['logged_in'] = True
        return redirect("/candidate_home")

    @app.route("/candidate_home/chats_candidate", methods=["POST"])
    @login_required
    def show_chats():
        message = MessageController()
        messages = message.get_all_messages_with_given_company_and_candidate(request.form["company"],
                                                                             session["candidate_id"])
        return render_template("messages.html", messages=messages)

    @app.route("/candidate_home/viewed")
    @login_required
    def show_viewed_jobs():
        controller = ViewedJobsByCandidateController()
        jobs = controller.get_all_jobs(session["candidate_id"])
        return render_template("all_jobs.html", jobs=jobs, viewed_liked="Viewed")

    @app.route("/candidate_home/liked")
    @login_required
    def show_liked_jobs():
        controller = LikedJobsByCandidateController()
        jobs = controller.get_all_jobs(session["candidate_id"])
        return render_template("all_jobs.html", jobs=jobs, viewed_liked="Liked")
   
    @app.route("/candidate_home/jobs", methods=["POST", "GET"])
    @login_required
    def show_new_job():
        controller = CandidateController()
        category_id = None
        if "category" in request.form:
            category_id = request.form["category"]
        else:
            category_id = request.args["category"]
        new_job = controller.get_job_by_category(session["candidate_id"], category_id)
        if new_job:
            return render_template("jobs.html", job=new_job)
        return render_template("too_picky.html")

    @app.route("/candidate_home/jobs/response", methods=["POST", "GET"])
    @login_required
    def candidate_responce():
        viewed = ViewedJobsByCandidateController()
        liked = LikedJobsByCandidateController()
        if request.method == 'POST':
            print(request.form['submit_button'])
            if request.form['submit_button'] == 'Like':
                liked.add_job(session["candidate_id"], request.form["job"])
            viewed.add_job(session["candidate_id"], request.form["job"])
        print(request.form)
        return redirect(url_for("show_new_job", category=request.form["category"]))
