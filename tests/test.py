import os
import unittest
from unittest.mock import patch

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

import redis
from redis.exceptions import ConnectionError

from hello import MainHandler


class TestApp(AsyncHTTPTestCase):
    def get_app(self):
        # Mock Redis connection
        with patch('redis.Redis') as mock_redis:
            # Configure mock Redis to return expected values
            mock_redis_instance = mock_redis.return_value
            mock_redis_instance.incr.return_value = 1

            # Create Tornado application
            handlers = [(r"/", MainHandler)]
            settings = {
                "template_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
                "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
            }
            return Application(handlers, **settings)

    def test_main_handler(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertIn(b"environment", response.body)
        self.assertIn(b"counter", response.body)

    def test_redis_connection_error(self):
        # Mock Redis connection error
        with patch('redis.Redis') as mock_redis:
            mock_redis.side_effect = ConnectionError

            response = self.fetch("/")
            self.assertEqual(response.code, 500)
            self.assertIn(b"Redis server isn't running", response.body)


if __name__ == "__main__":
    unittest.main()
