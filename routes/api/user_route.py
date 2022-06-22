from http import HTTPStatus

from flask import request

from errors.application_error import ApplicationError
from utilities.data_validation_utility import check_if_request_has_expected_content_type, \
    check_if_request_body_has_required_keys
from services.user_service import add_new_user, login_user


def api_user_registration():
    """
    function to register a new user via api
    :return: data of created user as json object
    """
    # check if request method is POST
    if request.method == "POST":
        # check for content type
        check_if_request_has_expected_content_type(__request=request, __content_type="application/json")

        # check if required keys are present in request body
        check_if_request_body_has_required_keys(__body=request.json,
                                                __keys={"user_full_name": True,
                                                        "user_dob": True,
                                                        "user_email": True,
                                                        "user_contact": True,
                                                        "user_password": True})

        # extract data from request body
        __full_name = request.json["user_full_name"]
        __dob = request.json["user_dob"]
        __email = request.json["user_email"]
        __contact = request.json["user_contact"]
        __password = request.json["user_password"]

        # add the user to database
        __new_user = add_new_user(__full_name=__full_name,
                                  __dob=__dob,
                                  __email=__email,
                                  __contact=__contact,
                                  __password=__password)

        # send response
        return {"user_id": __new_user.user_id}, HTTPStatus.CREATED
    else:
        raise ApplicationError(code=HTTPStatus.METHOD_NOT_ALLOWED,
                               message=f"request method not allowed: {request.method}")


def api_user_login():
    """
    function to sign in an existing user and generate json web token
    :return: generated json web token
    """
    if request.method == "POST":
        # check for content type
        check_if_request_has_expected_content_type(__request=request, __content_type="application/json")

        # check if required keys are present in request body
        check_if_request_body_has_required_keys(__body=request.json,
                                                __keys={"user_email": True,
                                                        "user_password": True})

        # extract data from request body
        __email = request.json["user_email"]
        __password = request.json["user_password"]

        # login user and get jwt
        __jwt = login_user(__email=__email, __password=__password)

        # send response
        return {"token": __jwt}, HTTPStatus.OK
    else:
        raise ApplicationError(code=HTTPStatus.METHOD_NOT_ALLOWED,
                               message=f"request method not allowed: {request.method}")

