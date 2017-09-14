#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from auth import auth
from Response import Response
import message_validator

app = Flask(__name__)

@app.route('/inbound/sms', methods=['POST'])
@auth.login_required
def inbound_sms():
    if not request.json:
        abort(400)
    response = message_validator.validate_message(request)
    if(response is not None and len(response.get_error()) > 0):
        return make_response(jsonify(response.__dict__),400)
    response = Response("inbound sms ok","")
    return make_response(jsonify(response.__dict__),200)

if __name__ == '__main__':
    app.run(debug=True)
