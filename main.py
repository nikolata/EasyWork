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

app = Flask(__name__)
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


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)
