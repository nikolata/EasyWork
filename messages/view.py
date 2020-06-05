from .controller import MessageController
from settings import app
from flask import session, request, render_template, redirect, url_for
from utls import login_required


class MessageView:
    @app.route("/candidate_home/add_message", methods=["POST"])
    @login_required
    def add_new_message():
        controller = MessageController()
        if "candidate_id" in session:
            if request.method == 'POST':
                if request.form['submit_button'] == 'Go back':
                    return redirect(url_for('candidate_home'))
            controller.add_message(request.form["company_id"], request.form["candidate_id"],
                                   1, request.form["message"])
        else:
            if request.method == 'POST':
                if request.form['submit_button'] == 'Go back':
                    return redirect(url_for('company_home'))
            controller.add_message(request.form["company_id"], request.form["candidate_id"],
                                   0, request.form["message"])

        messages = controller.get_messages(request.form["company_id"], request.form["candidate_id"])
        return render_template("messages.html", messages=messages)
