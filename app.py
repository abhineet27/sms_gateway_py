#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from flask.ext.login import LoginManager
from auth import auth
from Response import Response
import base64
import message_validator
import re
import app_redis

app = Flask(__name__)
login_manager = LoginManager()

@app.route('/inbound/sms', methods=['POST'])
@auth.login_required
@login_manager.request_loader
def inbound_sms():
    try:
        username = get_username_from_request(request)
        if not request.json:
            abort(400)
        response = message_validator.validate_message(request,username,True)
        if response is not None and len(response.get_error()) > 0:
            return make_response(jsonify(response.__dict__),400)
        if p.search(request.json['text']):
            app_redis.set(request.json['from']+request.json['to'],"STOP", 4*60*60)
        response = Response("inbound sms ok","")
        return make_response(jsonify(response.__dict__),200)
    except:
        response = Response("","unknown failure")
        return make_response(jsonify(response.__dict__),500)

@app.route('/outbound/sms', methods=['POST'])
@auth.login_required
@login_manager.request_loader
def outbound_sms():
    try:
        username = get_username_from_request(request)
        if not request.json:
            abort(400)
        response = message_validator.validate_message(request,username,False)
        if response is not None and len(response.get_error()) > 0:
            return make_response(jsonify(response.__dict__),400)
        if app_redis.get(request.json['to']+request.json['from']):
            response = Response("sms from "+request.json['from']+" to "+request.json['to']+" blocked by STOP request","")
            return make_response(jsonify(response.__dict__),400)
        if None == app_redis.get(request.json['from']) or int(app_redis.get(request.json['from'])) < 50:
            app_redis.update_cache(request.json['from'])
        else:
            response = Response("limit reached for from "+request.json['from'],"")
            return make_response(jsonify(response.__dict__),400)
        response = Response("outbound sms ok","")
        return make_response(jsonify(response.__dict__),200)
    except Exception as e:
        print e
        response = Response("","unknown failure")
        return make_response(jsonify(response.__dict__),500)

def get_username_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        api_key = base64.b64decode(api_key)
        username = api_key.split(':')[0]
        return username

p = re.compile(r'\bSTOP\b')

if __name__ == '__main__':
    app.run(debug=True)
