from .schemas import inventory_schema, inventories_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory, db
from . import inventory_bp
from app.extensions import cache
from sqlalchemy.orm import selectinload





@inventory_bp.route("/", methods=["POST"])
def add_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    query = select(Inventory).where(Inventory.name == inventory_data['name'])
    existing_inventory = db.session.execute(query).scalars().first()
    if existing_inventory:
        return jsonify({"message": "Inventory with this name already exists."}), 400

    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


@inventory_bp.route("/", methods=["GET"])
def get_inventories():
    query = select(Inventory)
    inventory = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventory)


@inventory_bp.route("/<int:id>", methods=["GET"])
def get_inventory(id):
    inventory = db.session.get(Inventory, id)
    return inventory_schema.jsonify(inventory), 200



@inventory_bp.route("/<int:id>", methods=["PUT"])
def update_inventory(id):
    inventory = db.session.get(Inventory, id)
    
    if not inventory:
        return jsonify({"message": "Inventory not found."}), 404

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)
        
    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route("/<int:id>", methods=["DELETE"])
def delete_inventory(id):
    inventory = db.session.get(Inventory, id)
    
    if not inventory:
        return jsonify({"message": "Inventory not found."}), 404
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": "Inventory deleted."}), 200