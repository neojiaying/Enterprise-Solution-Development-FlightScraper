from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/Airlines'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class airport_info(db.Model):
    __tablename__ = 'airport_info'

    iataCode = db.Column(db.String(128), primary_key = True)
    airportName = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)


    def __init__(self, iataCode, airportName, country):
        self.iataCode = iataCode
        self.airportName = airportName
        self.country = country
    
    def json(self):
        return {"iataCode" : self.iataCode, "airportName": self.airportName, "country": self.country}





