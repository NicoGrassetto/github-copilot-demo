import unittest
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Welcome to the Flask API!")

    def test_data(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, World!", response.get_json()["message"])

    def test_user(self):
        response = self.app.get('/user/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, testuser!", response.get_json()["message"])

    def test_query(self):
        response = self.app.get('/query?name=John&age=30')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, John!", response.get_json()["message"])
        self.assertEqual(response.get_json()["age"], "30")

    def test_submit(self):
        response = self.app.post('/submit', json={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Data received", response.get_json()["message"])

    def test_update(self):
        response = self.app.put('/update/1', json={"key": "new_value"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Data with id 1 updated", response.get_json()["message"])

    def test_delete(self):
        response = self.app.delete('/delete/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Data with id 1 deleted", response.get_json()["message"])

    def test_check_password(self):
        response = self.app.post('/check_password', json={"password": "Valid1Password"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Password is valid", response.get_json()["message"])

        response = self.app.post('/check_password', json={"password": "short"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password is too short", response.get_json()["message"])

        response = self.app.post('/check_password', json={"password": "NoDigitsHere"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password must contain at least one digit", response.get_json()["message"])

        response = self.app.post('/check_password', json={"password": "nouppercase1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password must contain at least one uppercase letter", response.get_json()["message"])

        response = self.app.post('/check_password', json={"password": "NOLOWERCASE1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password must contain at least one lowercase letter", response.get_json()["message"])

    def test_not_found(self):
        response = self.app.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.get_json()["message"])

    def test_bad_request(self):
        response = self.app.post('/submit', data="Invalid data")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid data", response.get_json()["message"])

if __name__ == '__main__':
    unittest.main()