from typing import List, Dict
import sys
import unittest
import xmlrunner
import tornado.testing
import json
from pprint import pprint

from utils import get_nearby_stores
from main import make_app

POSTCODE_1 = 'AL1 2RJ'
POSTCODE_2 = 'AL1 2DF'
POSTCODE_3 = 'AL9 5JP'
RAD_WIDE = 20000
LIMIT_WIDE = 10


class TestTask1(unittest.TestCase):
    def test_get_nearby_stores_wide_1(self):
        stores: List[Dict] = get_nearby_stores(POSTCODE_1, RAD_WIDE, LIMIT_WIDE, True)
        self.assertEqual(len(stores), 2)
        self.assertEqual([stores[0]['postcode'], stores[1]['postcode']], [POSTCODE_1, POSTCODE_2])

    def test_get_nearby_stores_wide_2(self):
        stores: List[Dict] = get_nearby_stores(POSTCODE_2, RAD_WIDE, LIMIT_WIDE, True)
        self.assertEqual(len(stores), 2)
        self.assertEqual([stores[0]['postcode'], stores[1]['postcode']], [POSTCODE_1, POSTCODE_2])

    def test_get_nearby_stores_wide_3(self):
        stores: List[Dict] = get_nearby_stores(POSTCODE_3, RAD_WIDE, LIMIT_WIDE, True)
        self.assertEqual(len(stores), 1)
        self.assertEqual([stores[0]['postcode']], [POSTCODE_3])


class TestTask2(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return '%s://localhost:%s%s' % (self.get_protocol(),
                                        self.get_http_port(), path)

    def test_br_page1(self):
        q: str = 'br'
        start_with: int = 0
        n: int = 3
        url: str = self.compose_url(q, start_with, n)
        response = self.fetch(url, method="GET")
        self.assertEqual(response.code, 200)

        data = json.loads(response.body.decode('utf-8'))
        # pprint(data)
        self.assertEqual(data['total_count'], 5)
        self.assertEqual(len(data['portion']), n)
        self.assertEqual(data['portion'][0]['postcode'], 'BR5 3RP')
        self.assertEqual(data['portion'][1]['name'], 'Bracknell')
        self.assertEqual(data['portion'][2]['name'], 'Brentford')

    def test_br_page2(self):
        q: str = 'br'
        start_with: int = 3
        n: int = 3
        url: str = self.compose_url(q, start_with, n)
        response = self.fetch(url, method="GET")
        self.assertEqual(response.code, 200)

        data = json.loads(response.body.decode('utf-8'))
        # pprint(data)
        self.assertEqual(data['total_count'], 5)
        self.assertEqual(len(data['portion']), 5 - n)
        self.assertEqual(data['portion'][0]['name'], 'Broadstairs')
        self.assertEqual(data['portion'][1]['name'], 'Tunbridge_Wells')

    def test_br_page3(self):
        q: str = 'br'
        start_with: int = 5
        n: int = 3
        url: str = self.compose_url(q, start_with, n)
        response = self.fetch(url, method="GET")
        self.assertEqual(response.code, 200)

        data = json.loads(response.body.decode('utf-8'))
        # pprint(data)
        self.assertEqual(data['total_count'], 5)
        self.assertEqual(len(data['portion']), 0)

    def compose_url(self, q: str, start_with: int, n: int) -> str:
        return '/task2?q={q}&start_with={start_with}&n={n}'.format(q=q, start_with=start_with, n=n)


if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    tests = test_loader.discover('.')
    runner = xmlrunner.XMLTestRunner(output='./test-results')
    res = not runner.run(tests).wasSuccessful()
    sys.exit(res)
