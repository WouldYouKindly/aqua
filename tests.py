import json
import unittest

from aqua.app import app, GLOBAL_DICTIONARY


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        GLOBAL_DICTIONARY._dict = {}

    def test_post_success(self):
        response = self.app.post('/dictionary',
                                 data=json.dumps({'key': 'key', 'value': 'value'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_post_wrong_request(self):
        response = self.app.post('/dictionary',
                                 data=json.dumps({'key': 'key'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_key_already_there(self):
        response1 = self.app.post('/dictionary',
                                 data=json.dumps({'key': 'key', 'value': 'value'}),
                                 content_type='application/json')
        response2 = self.app.post('/dictionary',
                                 data=json.dumps({'key': 'key', 'value': 'another'}),
                                 content_type='application/json')
        self.assertEqual(response2.status_code, 409)

    def test_get_success(self):
        key = 'key'
        value = 'value'

        self.app.post('/dictionary',
                      data=json.dumps({'key': key, 'value': value}),
                      content_type='application/json')

        response = self.app.get('/dictionary/%s' % key)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), value)

    def test_get_not_found(self):
        response = self.app.get('/dictionary/key')
        self.assertEqual(response.status_code, 404)

    def test_put_success(self):
        key = 'key'
        value = 'value'

        self.app.post('/dictionary',
                      data=json.dumps({'key': key, 'value': value}),
                      content_type='application/json')

        new_value = 'new value'
        response = self.app.put('/dictionary/%s' % key,
                                 data=json.dumps({'key': key, 'value': new_value}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_400(self):
        key = 'key'
        value = 'value'

        self.app.post('/dictionary',
                      data=json.dumps({'key': key, 'value': value}),
                      content_type='application/json')

        response = self.app.put('/dictionary/%s' % key,
                                data=json.dumps({'key': key}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_404(self):
        key = 'key'
        value = 'value'
        response = self.app.put('/dictionary/%s' % key,
                                data=json.dumps({'key': key, 'value': value}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_success(self):
        key = 'key'
        value = 'value'

        self.app.post('/dictionary',
                      data=json.dumps({'key': key, 'value': value}),
                      content_type='application/json')

        response = self.app.delete('/dictionary/%s' % key)
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['result'], value)

    def test_delete_not_found(self):
        response = self.app.delete('/dictionary/key')
        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data)
        self.assertEqual(response_json['result'], None)

if __name__ == '__main__':
    unittest.main()