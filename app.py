from datetime import datetime
from http import HTTPStatus
from flask import Flask
from dotenv import load_dotenv

from errors.application_error import ApplicationError
from routes.web.user_route import user_registration, user_login, user_logout, user_home
from routes.api.user_route import api_user_registration, api_user_login
from utilities.database_utility import DatabaseUtility
from utilities.environment_utility import get_environment_variable_value

# load dotenv
load_dotenv()

# create flask app
__app = Flask(import_name=__name__)

# add web url rules
__app.add_url_rule(rule="/register", view_func=user_registration, methods=["GET", "POST"])
__app.add_url_rule(rule="/login", view_func=user_login, methods=["GET", "POST"])
__app.add_url_rule(rule="/logout", view_func=user_logout, methods=["GET"])
__app.add_url_rule(rule="/", view_func=user_home, methods=["GET"])

# add api url rules
__app.add_url_rule(rule="/api/register", view_func=api_user_registration)
__app.add_url_rule(rule="/api/login", view_func=api_user_login)

# initialize database
DatabaseUtility.initialize_database_utility()

# add secret key
__app.secret_key = get_environment_variable_value(__env_var="APPLICATION_SECRET_KEY")


# add error handlers
@__app.errorhandler(code_or_exception=ApplicationError)
def handle_application_error(__err):
    return {"date": datetime.today(),
            "error-code": __err.error_code,
            "error-message": __err.error_message}, __err.error_code


@__app.errorhandler(code_or_exception=Exception)
def handle_error(__err):
    return {"date": datetime.today(),
            "error-code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "error-message": "some internal error occurred"}, HTTPStatus.INTERNAL_SERVER_ERROR


# start flask app
if __name__ == '__main__':
    __app.run(host="localhost", debug=True, load_dotenv=True)
