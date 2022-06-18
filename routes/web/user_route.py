from flask import request, render_template, redirect, flash, url_for

from services.user_service import add_new_user
from errors.application_error import ApplicationError


# view function for user registration
def user_registration():
    """
    function to register a new user via web
    :return:
    """
    # if GET request then send registration page
    if request.method == "GET":
        return render_template("user_registration.html")
    # if post request then process registration data
    elif request.method == "POST":
        try:
            add_new_user(__full_name=request.form.get("full-name"),
                         __dob=request.form.get("dob"),
                         __email=request.form.get("email"),
                         __contact=request.form.get("contact"),
                         __password=request.form.get("password"))
            return render_template("user_registration.html")
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("user_registration"))
