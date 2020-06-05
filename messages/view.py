from .controller import MessageController
from settings import app
from flask import session, request, render_template
from utls import login_required


class MessageView:
    @app.route("/candidate_home/add_message", methods=["POST"])
    @login_required    
    def add_new_message():
        controller = MessageController()
        if "candidate_id" in session:
            controller.add_message(request.form["company_id"], request.form["candidate_id"],
                                     1, request.form["message"])
        else:
            controller.add_message(request.form["company_id"], request.form["candidate_id"],
                                0, request.form["message"])
        messages = controller.get_messages(request.form["company_id"], request.form["candidate_id"])
        return render_template("messages.html", messages=messages)