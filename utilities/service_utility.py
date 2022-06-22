from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw
from flask import Response, Request
from jwt import encode
import uuid

from utilities.data_validation_utility import validate_date_format
from utilities.environment_utility import get_environment_variable_value


def convert_string_to_date(__date: str):
    """
    function to convert string to python datetime object
    :param __date: date value as string
    :return: equivalent datetime object
    """
    validate_date_format(__date=__date)
    return datetime.strptime(__date, "%Y-%m-%d")


def generate_random_id(__prefix: str = None):
    """
    function to generate random id with an optional prefix
    :param __prefix: string to add before randomly generated id
    :return: randomly generated uuid v4 with prefix added if given
    """
    if __prefix is None:
        return str(uuid.uuid4())
    else:
        return __prefix + str(uuid.uuid4())


def hash_text(__text: str):
    """
    function to hash a given string
    :param __text: string to hash
    :return: hashed string
    """
    return hashpw(password=__text.encode(encoding="utf-8"), salt=gensalt(rounds=12)).decode("utf-8")


def is_same_with_hashed_value(__hashed_value: str, __normal_value: str):
    """
    function to compare a given string with a corresponding hashed string
    :param __hashed_value: the hashed string to compare with
    :param __normal_value: the actual string to compare
    :return: True if both the strings are same, False otherwise
    """
    return checkpw(password=__normal_value.encode("utf-8"), hashed_password=__hashed_value.encode("utf-8"))


def generate_jwt(__payload: dict):
    """
    function to generate json web token from given payload
    :param __payload: payload to encode via json web token
    :return: generated json web token as string
    """
    __jwt_key = get_environment_variable_value("JWT_KEY")
    __jwt_algorithm = get_environment_variable_value("JWT_ALGORITHM")
    return encode(payload=__payload, key=__jwt_key, algorithm=__jwt_algorithm)


def store_jwt_into_browser_cookies(__response: Response, __jwt: str):
    """
    function to store jwt values into browser cookies
    :param __response: flask response object
    :param __jwt: json web token
    :return: None
    """
    # split jwt into parts
    __jwt_list = __jwt.strip().split(".")

    # store jwt into browser cookies
    for __itr in range(len(__jwt_list)):
        __response.set_cookie(key=str(__itr+1), value=__jwt_list[__itr])


def __get_jwt_from_browser_cookies(__request: Request):
    """
    function to get jwt values from browser cookies
    :param __request: flask request object
    :return: jwt value fetched from browser cookie, None otherwise
    """
    __token_list = []
    for __itr in range(3):
        __token_value = __request.cookies.get(key=str(__itr+1))
        if __token_value is None:
            return None
        else:
            __token_list.append(__token_value)
    return ".".join(__token_list)


def delete_jwt_cookie_from_browser(__response: Response):
    """
    function to remove jwt values from browser cookies
    :param __response: flask response object
    :return: None
    """
    for __itr in range(3):
        __response.set_cookie(key=str(__itr+1), value="", expires=0)


def is_user_signed_in(__request: Request):
    """
    function to check if a user is signed in
    :param __request: flask request object
    :return: True if the user is signed in, False otherwise
    """
    return __get_jwt_from_browser_cookies(__request=__request) is not None
