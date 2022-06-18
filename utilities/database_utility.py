from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, Session


class DatabaseUtility:
    """
    Database Utility: provides utility functions for database configuration
    """

    _database_engine: Engine = None
    _database_declarative_base = None

    @classmethod
    def _create_engine(cls):
        """
        function to create database engine
        :return: None
        """
        if cls._database_engine is None:
            cls._database_engine = create_engine(url="sqlite:///tj.db", echo=True)

    @classmethod
    def _create_base(cls):
        """
        function to create declarative base
        :return: None
        """
        if cls._database_declarative_base is None:
            cls._database_declarative_base = declarative_base()

    @classmethod
    def initialize_database_utility(cls):
        """
        function to initialize database utility service
        :return: None
        """
        cls._create_engine()
        cls._create_base()
        cls.get_declarative_base().metadata.create_all(cls._database_engine)

    @classmethod
    def get_declarative_base(cls):
        """
        function to get instance of declarative base
        :return: instance of database declarative base
        """
        if cls._database_declarative_base is None:
            cls._create_base()
        return cls._database_declarative_base

    @classmethod
    def get_session(cls):
        """
        function to get instance of database session
        :return: instance of database session
        """
        return Session(bind=cls._database_engine, autoflush=False, autocommit=False, expire_on_commit=False)
