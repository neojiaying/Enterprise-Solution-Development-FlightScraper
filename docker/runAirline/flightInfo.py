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

class flight_info(db.Model):
    __tablename__ = 'flight_info'

    flightId = db.Column(db.Integer, primary_key = True, autoincrement=True)
    flightNumber = db.Column(db.String(128), nullable=False)
    airlineId = db.Column(db.String(128), nullable=False)
    origin = db.Column(db.String(128), nullable=False)
    destination = db.Column(db.String(128), nullable=False)
    outbound = db.Column(db.String(128), nullable=False)
    inbound = db.Column(db.String(128), nullable=True)
    outbound_time = db.Column(db.String(128), nullable=False)
    inbound_time = db.Column(db.String(128), nullable=True)
    flightDuration = db.Column(db.Integer, nullable = True)
    seatsLeft = db.Column(db.Integer, nullable = True)
    price = db.Column(db.Float, nullable=False)
    Class = db.Column(db.String(128), nullable=True)

    def __init__(self, flightNumber, airlineId, origin, destination, outbound, inbound, outbound_time, inbound_time, flightDuration, seatsLeft, price, Class):
        self.flightNumber = flightNumber
        self.airlineId = airlineId
        self.origin = origin
        self.destination = destination
        self.outbound = outbound
        self.inbound = inbound
        self.outbound_time = outbound_time
        self.inbound_time = inbound_time
        self.flightDuration = flightDuration
        self.seatsLeft = seatsLeft
        self.price = price
        self.Class = Class

    def json(self):
        return {"flightId" : self.flightId, "flightNumber": self.flightNumber, "airlineId": self.airlineId, "origin": self.origin, "destination": self.destination, "outbound": self.outbound, "inbound": self.inbound, 
        "outbound_time": self.outbound_time, "inbound_time": self.inbound_time, "flightDuration": self.flightDuration, "seatsLeft": self.seatsLeft, "price": self.price, "Class": self.Class}
