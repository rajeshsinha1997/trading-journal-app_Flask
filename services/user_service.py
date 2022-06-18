from errors.application_error import ApplicationError
from utilities.data_validation_utility import validate_user_full_name, validate_date_format, is_date_is_in_range, \
    validate_email, validate_contact, validate_password
from utilities.service_utility import convert_string_to_date, generate_random_id, hash_text
from utilities.database_utility import DatabaseUtility
from repositories.user_repository import find_user_by_id, find_user_by_email, find_user_by_contact, insert_new_user
from schemas.database_schema import User

from dateutil.relativedelta import relativedelta
from datetime import datetime
from http import HTTPStatus


def add_new_user(__full_name: str, __dob: str, __email: str, __contact: str, __password: str):
    """
    function to add new user
    :param __full_name: full name of the user record to insert
    :param __dob: date of birth of the user record to insert
    :param __email: email of the user record to insert
    :param __contact: contact of the user record to insert
    :param __password: password of the user record to insert
    :return: instance of user schema
    """
    # validate given data
    validate_user_full_name(__full_name=__full_name)
    validate_date_format(__date=__dob)
    is_date_is_in_range(__date=convert_string_to_date(__dob),
                        __lower_limit=datetime.today() - relativedelta(years=100),
                        __upper_limit=datetime.today())
    validate_email(__email=__email)
    validate_contact(__contact=__contact)
    validate_password(__password=__password)

    # check if user with same email exists
    if find_user_by_email(__email=__email, __session=DatabaseUtility.get_session()) is not None:
        raise ApplicationError(code=HTTPStatus.CONFLICT,
                               message=f"user with same email already exists: {__email}")

    # check if user with same contact exists
    if find_user_by_contact(__contact=__contact, __session=DatabaseUtility.get_session()) is not None:
        raise ApplicationError(code=HTTPStatus.CONFLICT,
                               message=f"user with same contact already exists: {__contact}")

    # generate_user_id
    __user_id = generate_random_id(__prefix="user_")
    while find_user_by_id(__id=__user_id, __session=DatabaseUtility.get_session()) is not None:
        __user_id = generate_random_id(__prefix="user_")

    # create user object
    __user = User(user_id=__user_id,
                  user_full_name=__full_name,
                  user_dob=convert_string_to_date(__date=__dob),
                  user_email=__email,
                  user_contact=__contact,
                  user_password=hash_text(__text=__password),
                  user_email_verified=False,
                  user_contact_verified=False,
                  user_deleted=False)

    # insert user object to database
    insert_new_user(__user=__user, __session=DatabaseUtility.get_session())

    # return user object
    return __user
