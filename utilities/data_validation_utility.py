from datetime import datetime
from http import HTTPStatus
from re import compile
from flask import request

from errors.application_error import ApplicationError


def check_if_request_has_expected_content_type(__request: request, __content_type: str):
    """
    function to check if a request has expected content-type
    :param __request: instance of the request received
    :param __content_type: expected content type of the request
    :return: None
    """
    # check if request has a body with matching content type
    if not __request.headers.get('Content-Type') == __content_type:
        raise ApplicationError(code=HTTPStatus.BAD_REQUEST,
                               message=f"a valid request body of type {__content_type} is required")


def check_if_request_body_has_required_keys(__body: dict, __keys: list[str]):
    """
    function to validate if request body has required keys
    :param __body: request body data as dictionary
    :param __keys: keys to find in request body data
    :return: None
    """
    # check if all required keys are present in request body
    for __key in __keys:
        if __key not in __body:
            raise ApplicationError(code=HTTPStatus.BAD_REQUEST,
                                   message=f"{__key} is required")


def validate_user_full_name(__full_name: str):
    """
    function to validate user full name
    :param __full_name: full name value of user to be validated
    :return: None
    """
    # strip leading and trailing spaces from full name
    __temp = __full_name.strip().split(" ")

    # check if at least first and last names are provided
    if len(__temp) < 2:
        raise ApplicationError(code=HTTPStatus.BAD_REQUEST,
                               message="user must provide at least first and last name")

    # check if full name has any character other than alphabets
    for i in __temp:
        if not i.isalpha():
            raise ApplicationError(code=HTTPStatus.BAD_REQUEST, message="name can have only alphabets and spaces")


def validate_date_format(__date: str):
    """
    function to validate date
    :param __date: date value to be validated
    :return: None
    """
    # strip leading and trailing spaces
    __date = __date.strip()

    # check if date format is correct
    __temp = __date.split("-")
    for i in range(len(__temp)):
        if i == 0:
            if not len(__temp[i]) == 4:
                raise ApplicationError(code=HTTPStatus.BAD_REQUEST,
                                       message="invalid date, please provide date in format 'YYYY-MM-DD'")
        else:
            if not len(__temp[i]) == 2:
                raise ApplicationError(code=HTTPStatus.BAD_REQUEST,
                                       message="invalid date, please provide date in format 'YYYY-MM-DD'")


def is_date_is_in_range(__date: datetime, __lower_limit: datetime, __upper_limit: datetime):
    """
    function to check if date is in valid range
    :param __date: date value to be tested
    :param __lower_limit: lower limit of date allowed
    :param __upper_limit: upper limit of date allowed
    :return: None
    """
    # check date with lower limit
    if __date < __lower_limit:
        raise ApplicationError(code=HTTPStatus.INTERNAL_SERVER_ERROR,
                               message=f"given date can not be less than {__lower_limit}")

    # check date with upper limit
    if __date > __upper_limit:
        raise ApplicationError(code=HTTPStatus.INTERNAL_SERVER_ERROR,
                               message=f"given date can not be greater than {__upper_limit}")


def validate_email(__email: str):
    """
    function to validate email
    :param __email: email value to be validated
    :return: None
    """
    # strip leading and trailing spaces from email
    __email = __email.strip()

    # validate provided email
    if not compile("[a-zA-Z0-9_\.\+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-\.]+").match(__email):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "invalid email")


def validate_contact(__contact: str):
    """
    function to validate contact
    :param __contact: contact value to be validated
    :return: None
    """
    # strip leading and trailing spaces from contact
    __contact = __contact.strip()

    # check if contact has acceptable length
    if not len(__contact) == 10:
        raise ApplicationError(code=HTTPStatus.BAD_REQUEST, message="a contact number must have 10 digits")

    # validate provided contact
    if not compile("^[0-9]{10}").match(__contact):
        raise ApplicationError(HTTPStatus.BAD_REQUEST, "invalid contact number")


def validate_password(__password: str):
    """
    function to validate password
    :param __password: password value to be validated
    :return: None
    """
    # strip leading and trailing spaces
    __password = __password.strip()

    # check if password has valid length
    if len(__password) < 4:
        raise ApplicationError(code=HTTPStatus.BAD_REQUEST, message="a password should have at least 4 characters")
    elif len(__password) > 15:
        raise ApplicationError(code=HTTPStatus.BAD_REQUEST, message="a password should have at most 15 characters")
