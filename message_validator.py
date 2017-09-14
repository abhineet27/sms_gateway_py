from Response import Response

def validate_message(request):
    if not 'from' in request.json:
        response =  Response('','from is invalid')
        return response
    if len(request.json['from']) < 6 or len(request.json['from']) > 16:
        #return make_response(jsonify({'message':'','error': 'from is invalid'}), 400)
        response =  Response('','from is invalid')
        return response
