from app import app
import unittest


class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        #isolated test client like selenium
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    # Ensure that login page load correctly
    def test_login_page_loads(self):
        #isolated test client like selenium
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)
    # Ensure that login page load correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'you were just logged in', response.data)
    # Ensure that login page load correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentilals. please try again.', response.data)
    # Ensure that login out page load correctly
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            '/logout',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)
        
    # Ensure that the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)
    
    # Ensure that post show up on the main page    
    def test_post_show_up(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin",password="admin"),
            follow_redirects=True            
        )
        self.assertIn(b'name:',response.data)
       
    
if __name__ == '__main__':
    unittest.main()