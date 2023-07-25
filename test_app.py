import unittest
from website import create_app, db
from website.models import User


class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a test Flask app and configure it for testing
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        # Create the test database tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the test database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_sign_up1(self):
        # Send a POST request to the sign-up route with test user data
        data = {
            'email': 'test@example.com',
            'firstName': 'Test',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)

        # Check if the sign-up was successful (account created)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created!', response.data)

        # Check if the user was added to the database
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, 'Test')

    def test_sign_up2(self):
        # Send a POST request to the sign-up route with test user data
        data = {
            'email': 'test@example.com',
            'firstName': 'Test',
            'password1': 'p@ss1',
            'password2': 'p@ss1'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)

        # Check if the sign-up was successful or not
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password must be at least 7 characters.', response.data)

    def test_sign_up3(self):
        # Send a POST request to the sign-up route with test user data
        data = {
            'email': 'test@example.com',
            'firstName': 'test',
            'password1': 'p@ssword123',
            'password2': 'p@ssword321'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        # Check the flashed messages
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Passwords don&#39;t match.", response.data)

    def test_sign_up4(self):
        # Send a POST request to the sign-up route with test user data
        data = {
            'email': 'test@example.com',
            'firstName': '',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        
        # Check if the sign-up was successful or not
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'First name must be greater than 0 characters.', response.data)
    
    def test_sign_up5(self):
        # Register a new user
        data = {
            'email': 'test@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Logout the user
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'test@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email already exists.', response.data)

        
    
    def test_sign_up6(self):
        data = {
            'email': 'test@example.com',
            'firstName': 'test',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)

        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, 'test')
    

    def test_login(self):
        # Register a new user
        data = {
            'email': 'test@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Logout the user
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Login the user
        data = {
            'email': 'test@example.com',
            'password': 'p@ssword123'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login2(self):
        # Register a new user
        data = {
            'email': 'test@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Logout the user
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        data = {
            'email': 'test2@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Login the user
        data = {
            'email': 'test2@example.com',
            'password': 'p@ssword123'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login3(self):
        # Register a new user
        data = {
            'email': 'test@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Logout the user
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        #Register next user
        data = {
            'email': 'test2@example.com',
            'firstName': 'name',
            'password1': 'p@ssword123',
            'password2': 'p@ssword123'
        }
        response = self.client.post('/sign-up', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Login the user
        data = {
            'email': 'test2@example.com',
            'password': 'p@ssword123'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Logout the user
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Login the user
        data = {
            'email': 'test@example.com',
            'password': 'p@ssword123'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login4(self):
        data = {
            'email': 'test@example.com',
            'password': 'p@ssword123'
        }
        response = self.client.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email does not exist.', response.data)


    
if __name__ == '__main__':
    unittest.main()