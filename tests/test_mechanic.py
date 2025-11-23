import unittest
from app import create_app
from app.models import db, Mechanic



class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(
            name="Jane Doe",
            email="jane@email.com",
            salary="50000",
            phone="518-000-0004"
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()
        
        
class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.mechanic = Mechanic(
            name="Jane Doe",
            email="jane@email.com",
            salary="50000",
            phone="518-000-0004"
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()
        
        
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Julie Stewart",
            "email": "julie@email.com",
            "salary": "50000",
            "phone": "518-000-0005"
        }
        with self.app.app_context():
            response = self.client.post("/mechanics/", json=mechanic_payload)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['name'], 'Julie Stewart')
            
            
    def test_invalid_mechanic_creation(self):
        mechanic_payload = {
            "name": "",
            "salary": "50000",
            "phone": "123-456-7890"
        }
        with self.app.app_context():
            response = self.client.post("/mechanics/", json=mechanic_payload)
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn("email", data)
            self.assertIn("Missing data for required field.", data["email"])
            
            
    def test_get_mechanic(self):
        with self.app.app_context():
            mechanic_payload = {
                "name": "Julie Stewart",
                "email": "julie@email.com",
                "salary": "50000",
                "phone": "518-000-0005"
                }
            response = self.client.get('/mechanics/', json=mechanic_payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json[0]['name'], 'Jane Doe')
        
        
    def test_get_mechanic_by_id(self):
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Jane Doe')
        
        
    def test_mechanic_update(self):
        mechanic_payload = {
            "name": "Julie Stewart",
            "email": "stewart@email.com",
            "salary": "50000",
            "phone": "518-000-0004"
        }
        response = self.client.put('/mechanics/1', json=mechanic_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Julie Stewart')
        
        
    def test_mechanic_deletion(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        
        
    def test_most_tickets_mechanic(self):
        response = self.client.get('/mechanics/most_tickets')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Jane Doe')
        self.assertEqual(response.json[0]['tickets_worked'], 0)