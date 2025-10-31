from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, db, ServiceTicket
from . import customers_bp
from app.extensions import limiter
from app.utils.util import encode_token, token_required



@customers_bp.route("/login", methods=["POST"])
def login(): #login route that will create a token for the customer
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if customer and customer.password == password:
        auth_token = encode_token(customer.id)
        
        response = {
            "status": "success",
            "message": "successfully logged in",
            "auth_token": auth_token
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"message": "Invalid email or password!"}), 401
  


@customers_bp.route("/my-tickets", methods=["GET"])
@token_required #token required wrapper that validates the token and returns the customer id
def get_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    result = [
        {
            "vin":t.vin,
            "customer_id":t.customer_id,
            "mechanics":[{"id":m.id} for m in t.mechanics],
            "id":t.id,
            "service_description": t.service_description,
            "service_date": t.service_date
        }
        for t in tickets
    ]
    return jsonify({"tickets": result}), 200





@customers_bp.route("/", methods=["POST"])
@limiter.limit("5 per minute")# Limit to 5 requests per minute to prevent abuse
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
    try:
        page = int(request.args.get("page"))
        per_page = int(request.args.get("per_page"))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers.items), 200
    except:
        query = select(Customer)
        customers = db.session.execute(query).scalars().all()
    
        return customers_schema.jsonify(customers)


@customers_bp.route("/<int:id>", methods=["GET"])
def get_customer(id):
   customer = db.session.get(Customer, id)
   return customer_schema.jsonify(customer), 200
   


@customers_bp.route("/", methods=["PUT"])
@token_required #token is required to update customers info
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


@customers_bp.route("/", methods=["DELETE"])
@token_required #token is required to delete customer
def delete_customer(id):
    customer = db.session.get(Customer, id)
    
    if not customer:
        return jsonify({"message": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted."}), 200