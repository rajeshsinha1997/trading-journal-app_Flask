from sqlalchemy.orm import Session

from schemas.database_schema import User


def find_user_by_id(__id: str, __session: Session):
    """
    function to find user by id
    :param __id: id of the user record required to find
    :param __session: instance of the database session
    :return: user record if found with the id given, None otherwise
    """
    __result = __session.query(User).filter_by(user_id=__id).first()
    __session.close()
    return __result


def find_user_by_email(__email: str, __session: Session):
    """
    function to find user by email
    :param __email: email of the user record required to find
    :param __session: instance of the database session
    :return: user record if found with the email given, None otherwise
    """
    __result = __session.query(User).filter_by(user_email=__email).first()
    __session.close()
    return __result


def find_user_by_contact(__contact: str, __session: Session):
    """
    function to find user by contact
    :param __contact: contact of user record required to find
    :param __session: instance of the database session
    :return: user record if found with the contact given, None otherwise
    """
    __result = __session.query(User).filter_by(user_contact=__contact).first()
    __session.close()
    return __result


def insert_new_user(__user: User, __session: Session):
    """
    function to insert a new user record
    :param __user: user record to insert into database
    :param __session: instance of the database session
    :return: None
    """
    __session.add(__user)
    __session.commit()
    __session.close()
