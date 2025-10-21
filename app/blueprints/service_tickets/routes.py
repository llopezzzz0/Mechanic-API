from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer, Mechanic, ServiceTicket, db, mechanic_service_ticket
from . import service_tickets_bp



@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    if 'customer_id' not in service_ticket_data:
        return jsonify({"message": "customer_id is a required field"}), 400

    customer = db.session.get(Customer, service_ticket_data['customer_id'])
    if not customer:
        return jsonify({"message": "Invalid customer id"}), 400

    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201



@service_tickets_bp.route("/<int:ticket_id>/assign_mechanic/<int:mechanic_id>", methods=['PUT'])
def add_service_ticket_to_mechanic(ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not service_ticket:
        return jsonify({"message": "Invalid service ticket id"}), 400
    if not mechanic:
        return jsonify({"message": "Invalid mechanic id"}), 400

    db.session.execute(mechanic_service_ticket.insert().values(mechanic_id=mechanic.id, service_ticket_id=service_ticket.id))
    db.session.commit()
    return jsonify({"message": "Service ticket added to mechanic successfully"}), 200
   
    


@service_tickets_bp.route("/<int:ticket_id>/remove_mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_service_ticket_from_mechanic(mechanic_id, ticket_id):
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not service_ticket:
        return jsonify({"message": "Invalid service ticket id"}), 400
    if not mechanic:
        return jsonify({"message": "Invalid mechanic id"}), 400

    link = db.session.query(mechanic_service_ticket).filter_by(mechanic_id=mechanic.id, service_ticket_id=service_ticket.id).first()
    if not link:
        return jsonify({"message": "Service ticket is not assigned to this mechanic"}), 400


    db.session.execute(mechanic_service_ticket.delete().where(mechanic_service_ticket.c.mechanic_id == mechanic.id, mechanic_service_ticket.c.service_ticket_id == service_ticket.id))
    db.session.commit()

    return jsonify({"message": "Service ticket removed from mechanic successfully"}), 200





@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    mechanics = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(mechanics)