from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db
from . import customers_bp

@customers_bp.route("/", methods=["POST"])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer:
        return jsonify({"message": "Customer with this email already exists."}), 400
    
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    
    return customers_schema.jsonify(customers)


@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
   customer = db.session.get(Customer, id)
   return customer_schema.jsonify(customer), 200
   


@customers_bp.route("/<int:id>", methods=["PUT"])
def update_customer(id):
    customer = db.session.get(Customer, id)
    
    if not customer:
        return jsonify({"message": "Customer not found."}), 404

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
        
    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customers_bp.route("/<int:id>", methods=["DELETE"])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted."}), 200