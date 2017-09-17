import unittest
import sys
sys.path.append('../')
import auth
from my_sql import Account
from my_sql import Phone_Number
import message_validator
from flask import jsonify, json
from app import app
from mock import Mock
import app_redis

class AuthTest(unittest.TestCase):

    def test_get_password_negative_none(self):
        self.assertEqual(auth.get_password(None), None)

    def test_get_password_negative(self):
        self.assertEqual(auth.get_password(""), None)

    def test_get_password_positive(self):
        self.assertEqual(auth.get_password("plivo4"), "YHWE3HDLPQ")

    def test_unauthorized(self):
        with app.test_request_context('/'):
            self.assertEqual(auth.unauthorized().status_code, 403)

class AccountTest(unittest.TestCase):

    def test_account_with_exception(self):
        with self.assertRaises(Exception) as context:
            Account.get(Account.username == "dummy")
        self.assertTrue(True)

    def test_account_with_exception_none(self):
        with self.assertRaises(Exception) as context:
            Account.get(Account.username == None)
        self.assertTrue(True)

    def test_account_with_exception_by_id(self):
        with self.assertRaises(Exception) as context:
            Account.get(Account.id == 100)
        self.assertTrue(True)

    def test_account_with_valid_user_by_id1(self):
        self.assertEqual(Account.get(Account.id == 1).username, "plivo1")

    def test_account_with_valid_user_by_id2(self):
        self.assertEqual(Account.get(Account.id == 3).username, "plivo3")

    def test_account_with_valid_user(self):
        self.assertEqual(Account.get(Account.username == "plivo2").auth_id, "54P2EOKQ47")

class PhoneNumberTest(unittest.TestCase):

    def test_phone_number_with_exception(self):
        with self.assertRaises(Exception) as context:
            Phone_Number.get(Phone_Number.number == "dummy")
        self.assertTrue(True)

    def test_phone_number_with_exception_none(self):
        with self.assertRaises(Exception) as context:
            Phone_Number.get(Phone_Number.number == None)
        self.assertTrue(True)

    def test_phone_number_with_valid_phone_number_by_id1(self):
        self.assertEqual(Phone_Number.get(Phone_Number.id == 50).number, "441235330078")

    def test_phone_number_with_valid_phone_number_by_id2(self):
        self.assertEqual(Phone_Number.get(Phone_Number.id == 40).number, "441224980089")

    def test_phone_number_by_phone_number1(self):
        self.assertEqual(Phone_Number.get(Phone_Number.number == "61871112946").account_id, 3)

    def test_phone_number_by_phone_number2(self):
        self.assertEqual(Phone_Number.get(Phone_Number.number == "441224980092").account_id, 2)

    def test_phone_number_by_account_id_1(self):
        self.assertEqual(Phone_Number.get(Phone_Number.account_id == 1).id, 1)

    def test_phone_number_by_account_id_2(self):
        self.assertEqual(Phone_Number.get(Phone_Number.account_id == 4).id, 61)

class TestMessageValidator(unittest.TestCase):

    def test_validate_message_from_missing(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",True).error,"from is missing")

    def test_validate_message_to_missing(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",True).error,"to is missing")

    def test_validate_message_text_missing(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123456"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",True).error,"text is missing")

    def test_validate_message_to_not_found(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",True).error,"to parameter not found")

    def test_validate_message_to_not_found_wrong_combination(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "61881666914","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",True).error,"to parameter not found")

    def test_validate_message_from_not_found(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"from parameter not found")

    def test_validate_message_from_not_found_wrong_combination(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"61871232393","to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"from parameter not found")

    def test_validate_message_from_invalid1(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"","to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"from is invalid")

    def test_validate_message_from_invalid2(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"12345612345612345","to": "123456","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"from is invalid")

    def test_validate_message_to_invalid1(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"to is invalid")

    def test_validate_message_to_invalid2(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "12345612345612345","text":"test"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"to is invalid")

    def test_validate_message_text_invalid1(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123456","text":""}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"text is invalid")

    def test_validate_message_text_invalid2(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "123456","text":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}
            self.assertEqual(message_validator.validate_message(request,"plivo1",False).error,"text is invalid")

    def test_validate_message_inbound_valid1(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"123456","to": "61881666914","text":"xxxxxx"}
            self.assertEqual(message_validator.validate_message(request,"plivo4",True), None)

    def test_validate_message_inbound_valid2(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"441970450009","to": "61881666914","text":"xxxxxx"}
            self.assertEqual(message_validator.validate_message(request,"plivo4",True), None)

    def test_validate_message_outbound_valid1(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"61881666914","to": "123456","text":"xxxxxx"}
            self.assertEqual(message_validator.validate_message(request,"plivo4",False), None)

    def test_validate_message_outbound_valid2(self):
        with app.test_request_context('/'):
            request=Mock()
            request.json={"from":"61881666914","to": "441224980099","text":"xxxxxx"}
            self.assertEqual(message_validator.validate_message(request,"plivo4",False), None)


class TestAppRedis(unittest.TestCase):

    def test_set_get(self):
        app_redis.set("k","v",10)
        self.assertEqual(app_redis.get("k"),"v")

    def test_update_cache(self):
        app_redis.update_cache("k1")
        self.assertEqual(app_redis.get("k1"),'1')


if __name__ == '__main__':
    unittest.main()
