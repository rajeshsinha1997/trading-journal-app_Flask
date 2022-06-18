from flask import request

from utilities.data_validation_utility import check_if_request_has_expected_content_type, \
    check_if_request_body_has_required_keys
from services.user_service import add_new_user


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
                                                __keys=["user_full_name", "user_dob",
                                                        "user_email", "user_contact", "user_password"])

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
        return __new_user.user_id
