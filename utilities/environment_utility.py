from http import HTTPStatus
from os import environ

from errors.application_error import ApplicationError


def get_environment_variable_value(__env_var: str):
    """
    function to get environment variable value
    :param __env_var: environment variable name
    :return: value of environment variable
    """
    # fetch value from environment
    __value = environ[__env_var]

    # check if value was found
    if __value is None:
        raise ApplicationError(code=HTTPStatus.INTERNAL_SERVER_ERROR,
                               message=f"unknown environment variable: {__env_var}")
    else:
        return __value.strip()
