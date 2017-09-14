#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.login import LoginManager
from auth import auth
from Response import Response
import base64
import message_validator

app = Flask(__name__)
login_manager = LoginManager()

@app.route('/inbound/sms', methods=['POST'])
@auth.login_required
@login_manager.request_loader
def inbound_sms():
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        api_key = base64.b64decode(api_key)
        username = api_key.split(':')[0]
        print(username)
    if not request.json:
        abort(400)
    response = message_validator.validate_message(request)
    if(response is not None and len(response.get_error()) > 0):
        return make_response(jsonify(response.__dict__),400)
    response = Response("inbound sms ok","")
    return make_response(jsonify(response.__dict__),200)

if __name__ == '__main__':
    app.run(debug=True)
