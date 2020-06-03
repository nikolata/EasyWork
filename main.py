from database import Base, engine
import candidates.model
import companies.model
import jobs.model
import messages.model
# from jobs.model import JobModel
# from database import session_scope
# from index_view import CompanyCaller
from flask import Flask, render_template, redirect, url_for, request, flash, session
from functools import wraps
from companies.view import CompanyView
from candidates.view import CandidateView
from start import app

app.secret_key = '5Al6aSD}sy,$OZ_'


@app.route('/', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Sign up as company':
            return redirect(url_for('sign_up_as_company'))
        elif request.form['submit_button'] == 'Sign up as candidate':
            return redirect(url_for('sign_up_as_candidate'))
        elif request.form['submit_button'] == 'Log in':
            return redirect(url_for('log_in'))
    return render_template("welcome.html")


@app.route('/sign_up_as_company', methods=['POST', 'GET'])
def sign_up_as_company():
    view = CompanyView()
    return view.sign_up()


@app.route('/log_in', methods=['POST', 'GET'])
def log_in():
    company_view = CompanyView()
    error = None
    if request.method == 'POST':
        if company_view.log_in(email=request.form['email'], password=request.form['password']):
            session['logged_in'] = True
            return company_view.change_to_company_home()
        else:
            candidate_view = CandidateView()
            if candidate_view.log_in(email=request.form['email'], password=request.form['password']):
                session['logged_in'] = True
                return candidate_view.candidate_home()
            else:
                error = 'Wrong input!!!!'
    return render_template('log_in.html', error=error)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
