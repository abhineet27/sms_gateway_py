from Response import Response

def validate_message(request):
    if not 'from' in request.json:
        response =  Response('','from is missing')
        return response
    if len(request.json['from']) < 6 or len(request.json['from']) > 16:
        response =  Response('','from is invalid')
        return response
    if not 'to' in request.json:
        response =  Response('','to is missing')
        return response
    if len(request.json['to']) < 6 or len(request.json['to']) > 16:
        response =  Response('','to is invalid')
        return response
    if not 'text' in request.json:
        response =  Response('','text is missing')
        return response
    if len(request.json['text']) < 1 or len(request.json['text']) > 120:
        response =  Response('','text is invalid')
        return response
