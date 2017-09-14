from flask_httpauth import HTTPBasicAuth
from flask import make_response, jsonify
from my_sql import Account

auth = HTTPBasicAuth()

@auth.get_password
def get_password(user_name):
    for account in Account.filter(username=user_name):
        return account.auth_id
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
