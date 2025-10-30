from app .extensions import ma
from app.models import ServiceTicket
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True


class EditTicketSchema(ma.Schema):
    add_ids =fields.List(fields.Int(), load_default=[])
    remove_ids = fields.List(fields.Int(), load_default=[])
    class Meta:
        fields = ("add_ids", "remove_ids")
        
        

    
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
edit_ticket_schema = EditTicketSchema()