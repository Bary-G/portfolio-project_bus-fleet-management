from app.models.bus import Bus
from app.models.user import User
from app.models.base_model import BaseModel


class Route(BaseModel):
    def __init__(self, route_number, name, bus, user):
        super().__init__()
        self._route_number = self.string_validation(route_number, "route_number")
        self._name = self.name_validation(name)
        self._bus = self.bus_validation(bus)
        self._user = self.user_validation(user)

    @property
    def route_number(self):
        return self._route_number
    
    @route_number.setter
    def route_number(self, value):
        self._route_number = self.string_validation(value, "route_number")

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = self.name_validation(value)

    @property
    def user_id(self):
        return getattr(self._user, "id", None)

    @property
    def bus_id(self):
        return getattr(self._bus, "id", None)

    @staticmethod
    def string_validation(value, field_name, max_length=100):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")
        if not value:
            raise ValueError(f"{field_name} is required")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be less than {max_length} characters")
        return value

    @staticmethod
    def name_validation(name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name:
            raise ValueError("name is required")
        return name

    @staticmethod
    def bus_validation(bus):
        if not isinstance(bus, Bus):
            raise TypeError("bus must be a Bus instance")
        return bus

    @staticmethod
    def user_validation(user):
        if not isinstance(user, User):
            raise TypeError("user must be a User instance")
        return user
    
    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "route_number": self._route_number,
            "name": self._name,
            "bus": self._bus.to_dict() if hasattr(self._bus, "to_dict") else str(self._bus),
            "user": self._user.to_dict() if hasattr(self._user, "to_dict") else str(self._user)
        })
        return base_dict

