from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.reports import api as reports_ns
from app.api.v1.buses import api as buses_ns
from app.api.v1.routes import api as routes_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(reports_ns, path='/api/v1/reports')
    api.add_namespace(buses_ns, path='/api/v1/buses')
    api.add_namespace(routes_ns, path='/api/v1/routes')

    return app
