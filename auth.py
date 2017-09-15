from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from my_sql import Account

auth = HTTPBasicAuth()

@auth.get_password
def get_password(user_name):
    try:
        account = Account.get(Account.username == user_name)
        return account.auth_id
    except:
        return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
