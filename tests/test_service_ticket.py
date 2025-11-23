import unittest
from app import create_app
from app.models import db, ServiceTicket, Mechanic, Customer, Inventory
from datetime import date

class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.customer = Customer(
                name="Test User",
                email="test@email.com",
                password="test",
                phone="518-000-0000"
            )
            self.mechanic = Mechanic(
                name="Jane Doe",
                email="jane@email.com",
                phone="518-000-0004",
                salary="50000"
            )
            db.session.add_all([self.customer, self.mechanic])
            db.session.commit()
            self.ticket = ServiceTicket(
                vin="1HGCM826",
                service_description="This is a test service ticket",
                service_date=date(2024,1,1),
                customer_id= 1,
            )
            db.session.add(self.ticket)
            db.session.commit()
        self.client = self.app.test_client()
        
        
    def test_create_ticket(self):
        ticket_payload = {
            "vin": "2HGCM826",
            "service_description": "This is a new service ticket",
            "service_date": "2024-02-01",
            "customer_id":"1"
        }
        with self.app.app_context():
            response = self.client.post("/service_tickets/", json=ticket_payload)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json['vin'], '2HGCM826')
            
            
    def test_invalid_create_ticket(self):
        ticket_payload = {
            "vin": "2HGCM826",
            "service_description": "This is invalid",
            "service_date": "2024-02-01",
            "customer_id": 999
        }
        with self.app.app_context():
            response = self.client.post("/service_tickets/", json=ticket_payload)
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn("message", data)
        
        
    def test_get_service_tickets(self):        
        ticket_payload = ServiceTicket(
                vin= "1HGCM826",
                service_description="This is a test service ticket",
                service_date=date(2024,2,1),
                customer_id= 1
                )
        with self.app.app_context():    
            db.session.add(ticket_payload)
            db.session.commit()
            response = self.client.get("/service_tickets/")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(len(data),1)
            self.assertEqual(data[0]["id"], 1)
            
            
    def test_add_ticket_to_mechanic(self):
        ticket= ServiceTicket(
            vin="1HGCM826",
            service_description="tesing service ticket",
            service_date=date(2024,2,1),
            customer_id= "1"
        )
        mechanic = Mechanic(
            name = "Jane Doe",
            email = "j@email.com",
            salary = 50000,
            phone = "518-000-0004",
        )
        with self.app.app_context():
            db.session.add_all([ticket,mechanic])
            db.session.commit()
            response = self.client.put(f'/service_tickets/{ticket.id}/assign_mechanic/{mechanic.id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["message"] ,"Service ticket added to mechanic successfully")
        
        
    def test_remove_ticket_from_mechanic(self):
        ticket= ServiceTicket(
            vin="1HGCM826",
            service_description="tesing service ticket",
            service_date=date(2024,2,1),
            customer_id= "1"
        )
        mechanic = Mechanic(
            name = "Jane Doe",
            email = "j@email.com",
            salary = 50000,
            phone = "518-000-0004",
        )
        with self.app.app_context():
            db.session.add_all([ticket,mechanic])
            db.session.commit()
            ticket.mechanics.append(mechanic)
            response = self.client.put(f'/service_tickets/{ticket.id}/remove_mechanic/{mechanic.id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["message"] ,"Service ticket removed from mechanic successfully")
            
            
    def test_edit_ticket(self):
        with self.app.app_context():
            customer = Customer(
                name="Jessica Flowers",
                email="jessica@email.com",
                password="test",
                phone="518-000-0001"
            )
            db.session.add(customer)
            db.session.commit()
            mechanic = Mechanic(
                    name="Jane Doe",
                    email="janedoe@email.com",
                    phone="518-000-0004",
                    salary="50000"
                    )
            db.session.add(mechanic)
            db.session.commit()
            ticket= ServiceTicket(
                vin="1HGCM826",
                service_description="This is a test service ticket",
                service_date=date(2024,1,1),
                customer_id = customer.id
                )
            db.session.add(ticket)
            db.session.commit
            update_payload = {
                "remove_ids": [],
                "add_ids": [mechanic.id]
                }
            response = self.client.put(f"/service_tickets/{ticket.id}/edit", json=update_payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn(mechanic, ticket.mechanics)
            
            
    def test_add_inventory_to_ticket(self):
        with self.app.app_context():
            customer = Customer(
                name="Jessica Flowers",
                email="jessica@email.com",
                password="test",
                phone="518-000-0001"
            )
            db.session.add(customer)
            db.session.commit()
            inventory = Inventory(
                name = "brake light",
                price = "250.00"
            )
            db.session.add(inventory)
            db.session.commit()
            ticket = ServiceTicket(
                vin="1HGCM826",
                service_description="This is a test service ticket",
                service_date=date(2024,1,1),
                customer_id =customer.id
            )
            db.session.add(ticket)
            db.session.commit()
            response = self.client.put(f"/service_tickets/{ticket.id}/add_inventory/{inventory.id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(inventory, ticket.inventory)