import unittest
from app import create_app
from app.models import db, Inventory


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.inventory = Inventory(
                name="brake light",
                price = 250.00
            )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()
        
        
    def test_create_inventory(self):
        inventory_payload = {
            "name" : "brake light",
            "price" : "250.00"
            }
        with self.app.app_context():
            response = self.client.post("/inventory/", json=inventory_payload)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['name'], 'brake light')
            
            
    def test_get_inventory(self):
        inventory_payload = Inventory(
            name= "brake light",
            price= 250.00
        )
        with self.app.app_context():
            db.session.add(inventory_payload)
            db.session.commit()
            response = self.client.get("/inventory/")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(len(data), 1)
            self.assertEqual(data[0]["name"],"brake light")
            
            
    def test_get_inventory_by_id(self):
        inventory = Inventory(
            name = "brake light",
            price = 250.00
        )
        with self.app.app_context():
            db.session.add(inventory)
            db.session.commit()
            response = self.client.get('/inventory/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], 'brake light')
            
            
    def test_inventory_update(self):
        with self.app.app_context():
            item  = Inventory(
                name = "brake light",
                price = 250.00
                )
            db.session.add(item)
            db.session.commit()
            update_payload = {
                "name" : "light",
                "price": 200.00
            }
            response = self.client.put(f'/inventory/1', json=update_payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["name"], "light")
            self.assertEqual(float(data["price"]), 200.00)
            
            
    def test_inventory_deletion(self):
        with self.app.app_context():
            item  = Inventory(
                name = "brake light",
                price = 250.00
                )
            db.session.add(item)
            db.session.commit()
            response = self.client.delete('/inventory/1')
            self.assertEqual(response.status_code, 200)
            
            
    def test_invalid_inventory_deletion(self):
        with self.app.app_context():
            item  = Inventory(
                name = "brake light",
                price = 250.00
                )
            db.session.add(item)
            db.session.commit()
            response = self.client.delete('/inventory/90')
            self.assertEqual(response.status_code, 404)