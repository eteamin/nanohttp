
import unittest

import ujson

from nanohttp import Controller, html, HttpBadRequest, json
from nanohttp.tests.helpers import WsgiAppTestCase


class ExceptionTestCase(WsgiAppTestCase):

    class Root(Controller):
        @html
        def index(self):
            raise HttpBadRequest(reason='blah blah')

        @json
        def data(self):
            raise HttpBadRequest(reason='blah blah')

    def test_reason(self):
        response, content = self.assert_get('/', status=400)
        self.assertIn('x-reason', response)
        self.assertEqual(response['x-reason'], 'blah blah')
        
        response, content = self.assert_get('/data', status=400)
        self.assertIn('x-reason', response)
        self.assertEqual(response['x-reason'], 'blah blah')
        self.assertDictEqual(ujson.loads(content), {'description': '400 Bad Request', 'message': 'Bad Request'})


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
