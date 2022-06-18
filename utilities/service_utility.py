from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw
from jwt import encode
import uuid
import socket

from utilities.data_validation_utility import validate_date_format
from utilities.environment_utility import get_environment_variable_value


def get_current_ip_address():
    """
    function to get current machine's ip address
    :return: ip address of current machine
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def convert_string_to_date(__date: str):
    """
    function to convert string to date
    :param __date: date value as string
    :return: equivalent datetime object
    """
    validate_date_format(__date=__date)
    return datetime.strptime(__date, "%Y-%m-%d")


def generate_random_id(__prefix: str = None):
    """
    function to generate random id with an optional prefix
    :param __prefix: string to add before randomly generated id
    :return: randomly generated uuid v4
    """
    if __prefix is None:
        return str(uuid.uuid4())
    else:
        return __prefix + str(uuid.uuid4())


def hash_text(__text: str):
    """
    function to hash a given text
    :param __text: text to hash
    :return: hashed text
    """
    return hashpw(password=__text.encode(encoding="utf-8"), salt=gensalt(rounds=12))


def is_same_with_hashed_value(__hashed_value: str, __normal_value: str):
    """
    function to compare a given string with a corresponding hashed string
    :param __hashed_value: the hashed string to compare with
    :param __normal_value: the actual string to compare
    :return: True if both the strings are same, False otherwise
    """
    return checkpw(password=__normal_value.encode("utf-8"), hashed_password=bytes(__hashed_value))


def generate_jwt(__payload: dict):
    """
    function to generate json web token from given payload
    :param __payload: payload to encode via json web token
    :return: encoded json web token
    """
    __jwt_key = get_environment_variable_value("jwt_key")
    __jwt_algorithm = get_environment_variable_value("jwt_algorithm")
    return encode(payload=__payload, key=__jwt_key, algorithm=__jwt_algorithm)