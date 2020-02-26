import unittest
import app


class TestApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_open_main_page(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')
        self.assertIn(b'Generate Your Own Thomas G:Son Lyrics!', rv.data)


if __name__ == '__main__':
    unittest.main()
