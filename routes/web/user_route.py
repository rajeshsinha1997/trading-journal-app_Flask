from flask import request, render_template, redirect, flash, url_for, make_response

from services.user_service import add_new_user, login_user
from errors.application_error import ApplicationError
from utilities.service_utility import store_jwt_into_browser_cookies, is_user_signed_in, delete_jwt_cookie_from_browser


def user_registration():
    """
    function to register a new user via web
    :return: None
    """
    # if GET request then send registration page
    if request.method == "GET":
        # check if user is signed in
        if is_user_signed_in(__request=request):
            return redirect(url_for("user_home"))
        else:
            return render_template("user_registration.html")
    # if post request then process user registration
    elif request.method == "POST":
        try:
            # add new user with provided data
            add_new_user(__full_name=request.form.get("full-name"),
                         __dob=request.form.get("dob"),
                         __email=request.form.get("email"),
                         __contact=request.form.get("contact"),
                         __password=request.form.get("password"))
            # if registration is successful, redirect user to login page
            return redirect(url_for("user_login"))
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("user_registration"))


def user_login():
    """
    function to sign in a new user via web
    :return: None
    """
    # if GET request then send sign in page
    if request.method == "GET":
        # check if user is signed in
        if is_user_signed_in(__request=request):
            return redirect(url_for("user_home"))
        else:
            return render_template("user_login.html")
    # if POST request then process user sign in
    elif request.method == "POST":
        try:
            # sign in user and get json web token
            __jwt = login_user(__email=request.form.get("email"),
                               __password=request.form.get("password"))
            # create response and store json web token to cookies
            __response = make_response(redirect(url_for("user_home")))
            store_jwt_into_browser_cookies(__response=__response, __jwt=__jwt)

            # send response
            return __response
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("user_login"))


def user_logout():
    """
    function to sign out a user via web
    :return: None
    """
    # check if user is signed in
    if is_user_signed_in(__request=request):
        __response = make_response(redirect(url_for("user_login")))
        delete_jwt_cookie_from_browser(__response=__response)
        return __response
    else:
        return redirect(url_for("user_login"))


def user_home():
    """
    function to take user to user's home page
    :return:
    """
    if request.method == "GET":
        # check if user is signed in
        if is_user_signed_in(__request=request):
            return render_template("user_home.html", __user_signed_in=True)
        else:
            # redirect user to sign in page if not logged in
            return redirect(url_for("user_login"))
