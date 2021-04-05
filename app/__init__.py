from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)
resource = Resource

from app import view