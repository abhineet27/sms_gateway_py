import requests
import getpass
import unittest
from requests.auth import HTTPBasicAuth

class AppTest(unittest.TestCase):

    def test_inbound_sms_auth_fail(self):
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("test", "6DLH8A25XZ"),json={'from': '1234'})
        self.assertEqual(res.status_code,403)

    def test_inbound_sms_auth_success(self):
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"),json={'from': '123456','to':'61361220301','text':'abc'})
        self.assertEqual(res.status_code,200)

    def test_inbound_sms_bad_request1(self):
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"),json={})
        self.assertEqual(res.status_code,400)

    def test_inbound_sms_bad_request2(self):
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"))
        self.assertEqual(res.status_code,400)

    def test_inbound_sms_from_invalid1(self):
        request={'from': '1234','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is invalid')

    def test_inbound_sms_from_invalid2(self):
        request={'from': '12345612345612345','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is invalid')

    def test_inbound_sms_to_invalid1(self):
        request={'from': '123456','to':'123','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is invalid')

    def test_inbound_sms_to_invalid2(self):
        request={'from': '123456','to':'12345612345612345','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is invalid')

    def test_inbound_sms_text_invalid1(self):
        request={'from': '123456','to':'123456','text':''}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is invalid')

    def test_inbound_sms_text_invalid2(self):
        request={'from': '123456','to':'123456','text':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is invalid')

    def test_inbound_sms_from_missing(self):
        request={'to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is missing')

    def test_inbound_sms_to_missing(self):
        request={'from':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is missing')

    def test_inbound_sms_text_missing(self):
        request={'from':'61361220301','to':'61361220301'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is missing')

    def test_inbound_sms_to_parameter_not_found(self):
        request={'from':'61361220301','to':'123456','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to parameter not found')

    def test_inbound_sms_ok_without_stop(self):
        request={'from':'123456','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'inbound sms ok')

    def test_inbound_sms_ok_with_stop1(self):
        request={'from':'123456','to':'61361220301','text':'STOP, abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'inbound sms ok')

    def test_inbound_sms_ok_with_stop2(self):
        request={'from':'1234567','to':'61361220301','text':'STOP\r, abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'inbound sms ok')

    def test_inbound_sms_ok_with_stop3(self):
        request={'from':'323456','to':'61361220301','text':'STOP\n, abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'inbound sms ok')

    def test_inbound_sms_ok_with_stop4(self):
        request={'from':'333456','to':'61361220301','text':'STOP\r\n, abc'}
        res = requests.post('http://localhost:5000/inbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'inbound sms ok')

    def test_outbound_sms_auth_fail(self):
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("test", "6DLH8A25XZ"),json={'from': '1234'})
        self.assertEqual(res.status_code,403)

    def test_outbound_sms_auth_success(self):
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"),json={'from': '61361220301','to':'1113456','text':'abc'})
        self.assertEqual(res.status_code,200)

    def test_outbound_sms_bad_request1(self):
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"),json={})
        self.assertEqual(res.status_code,400)

    def test_outbound_sms_bad_request2(self):
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"))
        self.assertEqual(res.status_code,400)

    def test_outbound_sms_from_invalid1(self):
        request={'from': '1234','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is invalid')

    def test_outbound_sms_from_invalid2(self):
        request={'from': '12345612345612345','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is invalid')

    def test_outbound_sms_to_invalid1(self):
        request={'from': '123456','to':'123','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is invalid')

    def test_outbound_sms_to_invalid2(self):
        request={'from': '123456','to':'12345612345612345','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is invalid')

    def test_outbound_sms_text_invalid1(self):
        request={'from': '123456','to':'123456','text':''}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is invalid')

    def test_outbound_sms_text_invalid2(self):
        request={'from': '123456','to':'123456','text':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is invalid')

    def test_outbound_sms_from_missing(self):
        request={'to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from is missing')

    def test_outbound_sms_to_missing(self):
        request={'from':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'to is missing')

    def test_outbound_sms_text_missing(self):
        request={'from':'61361220301','to':'61361220301'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'text is missing')

    def test_outbound_sms_to_parameter_not_found(self):
        request={'from':'123456','to':'61361220301','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['error'],'from parameter not found')

    def test_outbound_sms_ok(self):
        request={'from':'61361220301','to':'123456444','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['message'],'outbound sms ok')

    def test_outbound_sms_stop_forbidden(self):
        request={'from':'61361220301','to':'123456','text':'abc'}
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo5", "6DLH8A25XZ"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,403)
        self.assertEqual(data['error'],'sms from 61361220301 to 123456 blocked by STOP request')

    def test_outbound_sms_limit_exceeded(self):
        request={'from':'4924195509192','to':'123456444','text':'abc'}
        for i in range(1,50):
            requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo1", "20S0KPNOIM"), json=request)
        res = requests.post('http://localhost:5000/outbound/sms', auth=HTTPBasicAuth("plivo1", "20S0KPNOIM"), json=request)
        data = res.json()
        self.assertEqual(res.status_code,403)
        self.assertEqual(data['error'],'limit reached for from 4924195509192')

if __name__ == '__main__':
    unittest.main()
