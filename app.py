from datetime import datetime
from http import HTTPStatus
from flask import Flask
from dotenv import load_dotenv

from errors.application_error import ApplicationError
from routes.web.user_route import user_registration
from routes.api.user_route import api_user_registration
from utilities.database_utility import DatabaseUtility
from utilities.environment_utility import get_environment_variable_value
from utilities.service_utility import get_current_ip_address

# load dotenv
load_dotenv()

# create flask app
__app = Flask(import_name=__name__)

# add web url rules
__app.add_url_rule(rule="/register", view_func=user_registration, methods=["GET", "POST"])

# add api url rules
__app.add_url_rule(rule="/api/register", view_func=api_user_registration, methods=["POST"])

# initialize database
DatabaseUtility.initialize_database_utility()

# add secret key
__app.secret_key = get_environment_variable_value(__env_var="application_secret_key")


# add error handlers
@__app.errorhandler(code_or_exception=ApplicationError)
def handle_application_error(__err):
    return {"date": datetime.today(),
            "error-code": __err.error_code,
            "error-message": __err.error_message}


@__app.errorhandler(code_or_exception=Exception)
def handle_error(__err):
    return {"date": datetime.today(),
            "error-code": HTTPStatus.INTERNAL_SERVER_ERROR,
            "error-message": "some internal error occurred"}


# start flask app
if __name__ == '__main__':
    __app.run(host="localhost", debug=True, load_dotenv=True)
