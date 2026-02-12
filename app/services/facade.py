from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.report import Report
from app.models.route import Route
from app.models.bus import Bus



class Facade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.bus_repo = InMemoryRepository()
        self.route_repo = InMemoryRepository()
        self.report_repo = InMemoryRepository()

    """user methods"""
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all() 
    
    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
    
    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.delete(user.id)
        return user

    """aeport methods"""
    def create_report(self, report_data):
        aeport = Report(**report_data)
        self.report_repo.add(aeport)
        return aeport

    def get_report(self, report_id):
        aeport = self.report_repo.get(report_id)
        if not aeport:
            return None
        return aeport

    def get_all_reports(self):
        return self.report_repo.get_all()

    def update_report(self, report_id, report_data):
        aeport = self.get_report(report_id)
        if not aeport:
            return None
        self.report_repo.update(report_id, report_data)
        return self.report_repo.get(report_id)
    
    def delete_report(self, report_id):
        aeport = self.get_report(report_id)
        if not aeport:
            return None
        self.report_repo.delete(report_id)
        return aeport

    """vehicle methods"""
    def create_bus(self, bus_data):
        if 'owner_id' in bus_data:
            owner = self.user_repo.get(bus_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            bus_data['owner'] = owner
            del bus_data['owner_id']

        reports_ids = bus_data.pop("reports", [])
        vehicle = Bus(**bus_data)
        self.bus_repo.add(vehicle)

        for aid in reports_ids:
            aeport = self.get_report(aid)
            if aeport:
                vehicle.add_report(aeport)

        return vehicle

    def get_bus(self, bus_id):
        vehicle = self.bus_repo.get(bus_id)
        if not vehicle:
            return None

        vehicle.owner = self.user_repo.get(vehicle.owner_id)
        vehicle.reports = [self.report_repo.get(aid) for aid in getattr(vehicle, 'report_ids', [])]
        return vehicle

    def get_all_buses(self):
        buses = self.bus_repo.get_all()
        for vehicle in buses:
            vehicle.owner = self.user_repo.get(vehicle.owner_id)
            vehicle.reports = [self.report_repo.get(aid) for aid in getattr(vehicle, 'report_ids', [])]
        return buses

    def update_bus(self, bus_id, bus_data):
        vehicle = self.get_bus(bus_id)
        if not vehicle:
            return None
        
        if 'owner_id' in bus_data:
            owner = self.get_user(bus_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            bus_data['owner'] = owner
            del bus_data['owner_id']

        if 'reports' in bus_data:
            valid_reports = []
            for report_id in bus_data['reports']:
                aeport = self.get_report(report_id)
                if not aeport:
                    raise ValueError(f"Report {report_id} does not exist")
                valid_reports.append(aeport)
            bus_data['reports'] = valid_reports

        self.bus_repo.update(bus_id, bus_data)
        return self.get_bus(bus_id)
    
    def delete_bus(self, bus_id):
        return self.bus_repo.delete(bus_id)

    """route methods"""
    def create_route(self, route_data):
       text = route_data.get('text')
       rating = route_data.get('rating')
       user_id = route_data.get('user_id')
       bus_id = route_data.get('bus_id')

       if not text or not isinstance(text, str):
           return None
       if not isinstance(rating, int) or not (1 <= rating <= 5):
           return None
       if not user_id or not bus_id:
           return None
       
       user = self.get_user(user_id)
       vehicle = self.get_bus(bus_id)
       if not user:
           raise ValueError("User not found")
       if not vehicle:
           raise ValueError("Vehicle not found")
       
       route = Route(text, rating, vehicle, user)
       self.route_repo.add(route)
       return route

    def get_route(self, route_id):
        return self.route_repo.get(route_id)

    def get_all_routes(self):
        return self.route_repo.get_all()

    def get_routes_by_bus(self, bus_id):
        all_routes = self.get_all_routes()
        matching_routes = []
        for route in all_routes:
            if route.bus_id == bus_id:
                matching_routes.append(route)
        return matching_routes

    def update_route(self, route_id, route_data):
        route = self.get_route(route_id)
        if not route:
            raise ValueError("Route not found")
        
        if 'rating' in route_data:
            rating = route_data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")

        if 'user_id' in route_data:
            user = self.get_user(route_data['user_id'])
            if not user:
                raise ValueError("User not found")
            route_data['user']= user
            del route_data['user_id']

        if 'bus_id' in route_data:
            vehicle= self.get_bus(route_data['bus_id'])
            if not vehicle:
                raise ValueError("Vehicle not found")
            route_data['bus_id'] = vehicle
            del route_data['bus_id']
        
        if 'text' in route_data:
            text = route_data['text']
            if not text or not isinstance(text, str):
                raise ValueError("Text is required")
        
        self.route_repo.update(route_id, route_data)
        return self.route_repo.get(route_id)

    def delete_route(self, route_id):
        self.route_repo.delete(route_id)
