from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('buses', description='Bus operations')

# Models for documentation only
report_model = api.model('BusReport', {
    'id': fields.String(description='Report ID'),
    'name': fields.String(description='Name of the report')
})

user_model = api.model('BusUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

bus_model = api.model('Bus', {
    'name': fields.String(required=True, description='Name of the bus'),
    'description': fields.String(description='Description of the bus'),
    'price': fields.Float(required=True, description='Price per night'),
    'length': fields.Float(required=True, description='Length of the bus'),
    'engine_type': fields.String(required=True, description='Engine type'),
    'euro_standard': fields.Integer(required=True, description='Euro standard'),
    'status': fields.Integer(required=True, description='Status (-1 retired, 0 off, 1 active)'),
    'owner_id': fields.String(required=True, description='Owner ID'),
    'routes': fields.List(fields.String, required=True, description="List of route IDs"),
    'reports': fields.List(fields.String, required=True, description="List of report IDs")
})

@api.route('/')
class BusList(Resource):

    @api.expect(bus_model)
    @api.response(201, 'Bus successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = request.json
        if not data:
            return {'error': 'Invalid input data'}, 400

        # Validate owner
        owner_id = data.get('owner_id')
        if not facade.get_user(owner_id):
            return {'error': f"Owner with ID {owner_id} does not exist"}, 400

        # Validate reports
        for report_id in data.get('reports', []):
            if not facade.get_report(report_id):
                return {'error': f"Report with ID {report_id} does not exist"}, 400

        try:
            new_bus = facade.create_bus(data)
            return new_bus.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of buses retrieved successfully')
    def get(self):
        buses = facade.get_all_buses()
        return {'buses': [bus.to_dict() for bus in buses]}, 200


@api.route('/<string:bus_id>')
class BusResource(Resource):

    @api.response(200, 'Bus details retrieved successfully')
    @api.response(404, 'Bus not found')
    def get(self, bus_id):
        bus = facade.get_bus(bus_id)
        if not bus:
            return {'error': 'Bus not found'}, 404
        return bus.to_dict(), 200

    @api.expect(bus_model)
    @api.response(200, 'Bus updated successfully')
    @api.response(404, 'Bus not found')
    @api.response(400, 'Invalid input data')
    def put(self, bus_id):
        data = request.get_json()
        if not data:
            return {'error': 'Invalid input data'}, 400

        # Validate owner
        owner_id = data.get('owner_id')
        if owner_id and not facade.get_user(owner_id):
            return {'error': f"Owner with ID {owner_id} does not exist"}, 400

        # Validate reports
        for report_id in data.get('reports', []):
            if not facade.get_report(report_id):
                return {'error': f"Report with ID {report_id} does not exist"}, 400

        # Basic validation
        if 'name' in data and not isinstance(data['name'], str):
            return {'error': 'name must be a string'}, 400
        if 'price' in data and data['price'] <= 0:
            return {'error': 'price must be positive'}, 400

        try:
            updated_bus = facade.update_bus(bus_id, data)
            if not updated_bus:
                return {'error': 'Bus not found'}, 404
            return updated_bus.to_dict(), 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Bus deleted successfully')
    @api.response(404, 'Bus not found')
    def delete(self, bus_id):
        bus = facade.get_bus(bus_id)
        if not bus:
            return {'error': 'Bus not found'}, 404
        facade.delete_bus(bus_id)
        return {'message': 'Bus deleted successfully'}, 200
