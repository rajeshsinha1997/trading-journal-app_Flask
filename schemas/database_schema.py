from sqlalchemy import Column, String, Boolean, Date

from utilities.database_utility import DatabaseUtility


class User(DatabaseUtility.get_declarative_base()):
    """
    User schema: represents users table in database
    """
    __tablename__ = "users"

    user_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    user_full_name = Column(type_=String(100), nullable=False)
    user_dob = Column(type_=Date, nullable=False)
    user_email = Column(type_=String(100), unique=True, nullable=False, index=True)
    user_contact = Column(type_=String(10), unique=True, nullable=False, index=True)
    user_password = Column(type_=String(100), nullable=False)
    user_email_verified = Column(type_=Boolean, nullable=False, default=False)
    user_contact_verified = Column(type_=Boolean, nullable=False, default=False)
    user_deleted = Column(type_=Boolean, nullable=False, default=False)
