"""
Test Suite Playground

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
"""
import unittest
from app import app

class TestAppService(unittest.TestCase):
    """ App Server Tests """

    def setUp(self):
        """ Runs before each test """
        self.app = app.test_client()

    def test_index(self):
        """ Test the Home Page """
        # resp = self.app.get("/")
        # self.assertEqual(resp.status_code, 200)
        # data = resp.get_json()
        # self.assertEqual(data["message"], "My API Service")

if __name__ == "__main__":
    unittest.main()
