from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanic, db
from . import mechanics_bp





@mechanics_bp.route("/", methods=["POST"])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({"message": "Mechanic with this email already exists."}), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)


@mechanics_bp.route("/<int:id>", methods=["GET"])
def get_mechanic(id):
   mechanic = db.session.get(Mechanic, id)
   return mechanic_schema.jsonify(mechanic), 200
   


@mechanics_bp.route("/<int:id>", methods=["PUT"])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found."}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
        
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:id>", methods=["DELETE"])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted."}), 200