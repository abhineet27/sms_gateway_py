import peewee
from peewee import *

db = MySQLDatabase('sms_gateway', host="localhost", port=3306, user='root', passwd='root')

class Account(peewee.Model):
    username = peewee.TextField()
    auth_id = peewee.TextField()

    class Meta:
        database = db
class Phone_Number(peewee.Model):
    number = peewee.TextField()
    account_id = peewee.IntegerField()

    class Meta:
        database = db
