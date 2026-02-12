from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('routes', description='Route operations')

# Define the route model for input validation and documentation
route_model = api.model('Route', {
    'route_number': fields.String(required=True, description='Route number of the route'),
    'name': fields.String(required=True, description='Name of the route'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'bus_id': fields.List(fields.String, required=True, description='List of bus IDs')
})

@api.route('/')
class RouteList(Resource):

    @api.expect(route_model)
    @api.response(201, 'Route successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new route"""
        data_route = api.payload or {}

        route_number = data_route.get('route_number')
        name = data_route.get('name')
        user_id = data_route.get('user_id')
        bus_id = data_route.get('bus_id')

        # Validations
        if not route_number or not isinstance(route_number, str):
            return {'error': 'route_number must be a non-empty string'}, 400

        if not name or not isinstance(name, str):
            return {'error': 'name must be a non-empty string'}, 400

        if not user_id:
            return {'error': 'user_id is required'}, 400

        if not isinstance(bus_id, list) or not bus_id:
            return {'error': 'bus_id must be a non-empty list of bus IDs'}, 400

        # Create route
        new_route = facade.create_route({
            'route_number': route_number,
            'name': name,
            'user_id': user_id,
            'bus_id': bus_id
        })

        if not new_route:
            if not facade.get_user(user_id):
                return {'error': 'User not found'}, 400
            # bus_id is a list → check each bus
            for b in bus_id:
                if not facade.get_bus(b):
                    return {'error': f'Bus not found: {b}'}, 400
            return {'error': 'Could not create route'}, 400

        return {
            'id': new_route.id,
            'route_number': new_route.route_number,
            'name': new_route.name,
            'user_id': new_route.user_id,
            'bus_id': new_route.bus_id
        }, 201

    @api.response(200, 'List of routes retrieved successfully')
    def get(self):
        """Retrieve a list of all routes"""
        routes = facade.get_all_routes()
        return [
            {
                'id': route.id,
                'route_number': route.route_number,
                'name': route.name
            }
            for route in routes
        ], 200


@api.route('/<route_id>')
class RouteResource(Resource):

    @api.response(200, 'Route details retrieved successfully')
    @api.response(404, 'Route not found')
    def get(self, route_id):
        """Get route details by ID"""
        route = facade.get_route(route_id)
        if not route:
            return {'error': 'Route not found'}, 404

        return {
            'id': route.id,
            'route_number': route.route_number,
            'name': route.name,
            'user_id': route.user_id,
            'bus_id': route.bus_id
        }, 200

    @api.expect(route_model)
    @api.response(200, 'Route updated successfully')
    @api.response(404, 'Route not found')
    @api.response(400, 'Invalid input data')
    def put(self, route_id):
        """Update a route's information"""
        data_route = api.payload or {}

        if 'route_number' in data_route:
            if not isinstance(data_route['route_number'], str) or not data_route['route_number']:
                return {'error': 'route_number must be a non-empty string'}, 400

        if 'name' in data_route:
            if not isinstance(data_route['name'], str) or not data_route['name']:
                return {'error': 'name must be a non-empty string'}, 400

        if 'bus_id' in data_route:
            if not isinstance(data_route['bus_id'], list) or not data_route['bus_id']:
                return {'error': 'bus_id must be a non-empty list of bus IDs'}, 400

        updated_route = facade.update_route(route_id, data_route)

        if not updated_route:
            if not facade.get_route(route_id):
                return {'error': 'Route not found'}, 404
            return {'error': 'Invalid input data'}, 400

        return {'message': 'Route updated successfully'}, 200

    @api.response(200, 'Route deleted successfully')
    @api.response(404, 'Route not found')
    def delete(self, route_id):
        """Delete a route"""
        route = facade.get_route(route_id)
        if not route:
            return {'error': 'Route not found'}, 404

        facade.delete_route(route_id)
        return {'message': 'Route deleted successfully'}, 200


@api.route('/buses/<bus_id>/routes')
class BusRouteList(Resource):

    @api.response(200, 'List of routes for the bus retrieved successfully')
    @api.response(404, 'Bus not found')
    def get(self, bus_id):
        bus = facade.get_bus(bus_id)
        if not bus:
            return {'error': 'Bus not found'}, 404

        bus_routes = facade.get_routes_by_bus(bus_id)

        return [
            {
                'id': route.id,
                'route_number': route.route_number,
                'name': route.name
            }
            for route in bus_routes
        ], 200
