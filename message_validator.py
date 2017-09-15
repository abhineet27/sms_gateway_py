from Response import Response
from my_sql import Phone_Number
from my_sql import Account

def validate_message(request,username,is_inbound):
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
    if is_inbound:
        try:
            account = Account.get(Account.username == username)
            phoneNumber = Phone_Number.get(Phone_Number.number == request.json['to'])
            if account.id != phoneNumber.account_id:
                response =  Response('','to parameter not found')
                return response
        except Exception as e:
            response =  Response('','to parameter not found')
            return response
    else:
        try:
            account = Account.get(Account.username == username)
            phoneNumber = Phone_Number.get(Phone_Number.number == request.json['from'])
            if account.id != phoneNumber.account_id:
                response =  Response('','from parameter not found')
                return response
        except Exception as e:
            response =  Response('','from parameter not found')
            return response
