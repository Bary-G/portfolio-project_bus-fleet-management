from app.models.base_model import BaseModel
from app.models.user import User
from app.models.report import Report


class Bus(BaseModel):
    """Class representing a Bus entity"""

    def __init__(self, name, engine_type, euro_standard, routes=[], reports=[], description="", price=0.0, length=0.0,
                 status=0, capacity=0.0, owner=None):
        super().__init__()
        self._name = name
        self.description = description
        self._price = price
        self._length = length
        self._engine_type = engine_type
        self._euro_standard = euro_standard
        self._capacity = capacity
        self._status = status
        self._owner = owner
        self.owner_id = owner.id if owner else None
        self.routes = routes
        self.reports = reports

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) > 100:
            raise ValueError("Name too long")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if not (0 < value <= 24.5):
            raise ValueError("Length must be between 0 and 24.5 meters")
        self._length = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if value < 0:
            raise ValueError("Capacity must be positive")
        self._capacity = value

    @property
    def engine_type(self):
        return self._engine_type

    @engine_type.setter
    def engine_type(self, value):
        allowed = {"thermal", "hybrid", "hydrogen", "electric"}
        if not isinstance(value, str) or value not in allowed:
            raise TypeError("Engine_type must be thermal, hybrid, hydrogen or electric")
        self._engine_type = value

    @property
    def euro_standard(self):
        return self._euro_standard

    @euro_standard.setter
    def euro_standard(self, value):
        if not isinstance(value, int) or value < 0:
            raise TypeError("euro_standard must be a positive integer")
        self._euro_standard = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if not isinstance(value, int) or not (-1 <= value <= 1):
            raise TypeError("status must be an integer between -1 and 1")
        self._status = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if value is not None and not isinstance(value, User):
            raise TypeError("Owner must be a User")
        self._owner = value
        self.owner_id = value.id if value else None

    def add_route(self, route):
        from app.models.route import Route
        if not isinstance(route, Route):
            raise TypeError("route must be a Route instance")
        self.routes.append(route)

    def add_report(self, report):
        from app.models.report import Report
        if not isinstance(report, Report):
            raise TypeError("report must be a Report instance")
        self.reports.append(report)

    def update(self, data: dict):
        for key, value in data.items():

            if key == 'price' and value < 0:
                raise ValueError("price must be positive")

            elif key == 'length' and not (0 < value <= 24.5):
                raise ValueError("length must be between 0 and 24.5")

            elif key == 'capacity' and value < 0:
                raise ValueError("capacity must be positive")

            elif key == 'name':
                if not isinstance(value, str):
                    raise TypeError("name must be a string")
                if len(value) > 100:
                    raise ValueError("name must be <= 100 characters")

            elif key == 'owner':
                if value is not None and not isinstance(value, User):
                    raise TypeError("owner must be a User instance")

            if hasattr(self, key):
                setattr(self, key, value)

        self.save()

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "length": self.length,
            "capacity": self.capacity,
            "engine_type": self.engine_type,
            "euro_standard": self.euro_standard,
            "status": self.status,
            "owner_id": self.owner.id if self.owner else None,
            "routes": [route.id for route in self.routes],
            "reports": [report.id for report in self.reports]
        })
        return base_dict
