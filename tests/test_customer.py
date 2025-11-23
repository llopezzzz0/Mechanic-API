import unittest
from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.customer = Customer(
            name="Test User",
            email="test@email.com",
            password="test",
            phone="518-000-0000"
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
        
        
    def test_create_customer(self):
        customer_payload = {
            "name": "New User",
            "email": "new@email.com",
            "password": "test",
            "phone": "518-000-0001"
        }
        with self.app.app_context():
            response = self.client.post("/customers/", json=customer_payload)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['name'], 'New User')
            
            
    def test_invalid_customer_creation(self):
        customer_payload = {
            "name": "Jane",
            "password": "123",
            "phone": "123-456-7890"
        }
        response = self.client.post("/customers/", json=customer_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("email", data)
        self.assertIn("Missing data for required field.", data["email"])
            
            
    def test_login_customer(self):
        customer_payload = {
            "email": "test@email.com",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=customer_payload)
        self.assertEqual(response.status_code, 200)
        return response.json['auth_token']
        
        
    def test_invalid_cutomer_login(self):
        customer_payload = {
            "email": "",
            "password": "test"
        }
        response = self.client.post('/customers/login', json=customer_payload)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("message", data)
        self.assertIn("Invalid email or password!", data["message"])
    
    
    def test_get_customer(self):
        response = self.client.get('/customers/?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'Test User')
        
        
    def test_get_customer_by_id(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Test User')
        
        
    def test_get_tickets(self):
        headers= {'Authorization': f'Bearer {self.token}'}
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['tickets'], [])
        
        
    def test_customer_update(self):
        update_payload = {
            "name": "Updated User",
            "email": "lol@email.com",
            "password": "",
            "phone": ""
        }
        headers = {'Authorization': f"Bearer {self.test_login_customer()}"}
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Updated User')
        self.assertEqual(response.json['email'], 'lol@email.com')
        
        
    def test_customer_deletion(self):
        headers = {'Authorization': f"Bearer {self.test_login_customer()}"}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)