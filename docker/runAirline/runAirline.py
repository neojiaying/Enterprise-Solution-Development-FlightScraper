from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flightInfo import flight_info
from airportInfo import airport_info
from flask_cors import CORS

from os import environ

import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/airlines'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/airlines'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://bfnyyievvpmzxo:f00e9a52b665e400420bdfd59bdb764ded194dcfe543a3a4a1cafc60aab0c8f4@ec2-35-174-88-65.compute-1.amazonaws.com:5432/dductjgrep939t"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

@app.route("/runAirline/airline/<string:origin>&<string:destination>&<string:outbound>&<string:inbound>")
def search_by_filter(origin, destination, outbound, inbound):
    # return jsonify({"flightinfo": [fligthflightInfo.json() for flightInfo in flight_info.query.filter_by(origin=origin, destination=destination, outbound=outbound, inbound=inbound).all()]})
    # print(({"flight_info": [flightInfo.json() for flightInfo in flight_info.query.filter_by(origin=origin, destination=destination, outbound=outbound, inbound=inbound).all()]}))
    return jsonify({"flight_info": [flightInfo.json() for flightInfo in flight_info.query.filter_by(origin=origin, destination=destination, outbound=outbound, inbound=inbound).all()]})
    # flightInfo = flight_info.query.filter_by(origin=origin, destination=destination, outbound=outbound, inbound=inbound).first()
    # if flightInfo:
    #     return jsonify(flightInfo.json())
    # return jsonify({"message": "flights not found."}), 404

@app.route("/runAirline/airline")
def get_all():
    return jsonify({"airport_info": [airport_info.json() for airport_info in airport_info.query.all()]})

@app.route("/runAirline/getallflightinfo")
def getAllFlightInfo():
    return jsonify({"flight_info": [flightInfo.json() for flightInfo in flight_info.query.all()]})

@app.route("/runAirline/get_one_flight/<string:flightID>")
def get_one_flight(flightID):
    try:
        flightInfo = flight_info.query.filter_by(flightId = flightID).first()
        if flightInfo:
            return jsonify(flightInfo.json())
    except Exception as e:
        print(e.args)
    
    return jsonify({"message": "flights not found."}), 404

@app.route("/runAirline/airline/<string:iataCode>")
def get_airport_info(iataCode): 
    airportInfo = airport_info.query.filter_by(iataCode = iataCode).first()
    if airportInfo:
        return jsonify(airportInfo.json())
    return jsonify({"message": "airport not found."}), 404

@app.route("/runAirline/addFlight", methods=['POST'])
def addFlight():
    data = request.get_json()
    flight = flight_info(**data)

    try:
        db.session.add(flight)
        db.session.commit()
    except Exception as inst:
        return jsonify({"message": "An error occurred while adding the flight."}), 500
    return jsonify({"message": "Success"}), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)




    