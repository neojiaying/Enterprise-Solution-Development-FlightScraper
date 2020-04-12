import random
import json
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from flask_cors import CORS
from os import environ
import requests
import psycopg2

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/passenger'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/passenger'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://oicchxookeyjav:ec6721556f4d16f38c62b547d7faf9d0d86facceefb6bc826310db939d0f9ba1@ec2-34-202-7-83.compute-1.amazonaws.com:5432/d1m8mmr4p9n4lf')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# bookingURL = "http://g8t2-booking.herokuapp.com/booking"


# Use a language-level function call to enable interaction with error_handling
#import error_handling

#error_handlingURL = "http://localhost:5003/error_handling"


class Passenger(db.Model):
    __tablename__ = 'passenger_info'

    passengerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    passportNo = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    DOB = db.Column(db.String(128), nullable=False)
    bookingID = db.Column(db.Integer, nullable=False)
    addonsID = db.Column(db.String, nullable=True)
    parentPassengerID = db.Column(db.Integer, nullable=False)
    membership_no = db.Column(db.String(128), nullable=True)
    price = db.Column(db.String(128), nullable=False)
    seatNo = db.Column(db.String(128), nullable=False)

    def __init__(self, passportNo, name, email, DOB, bookingID, addonsID, parentPassengerID, membership_no, price, seatNo):
        self.passportNo = passportNo
        self.name = name
        self.email = email
        self.DOB = DOB
        self.bookingID = bookingID
        self.addonsID = addonsID
        self.parentPassengerID = parentPassengerID
        self.membership_no = membership_no
        self.price = price
        self.seatNo = seatNo

    def json(self):
        return {"passengerID": self.passengerID, "passportNo": self.passportNo,
                "name": self.name, "email": self.email, "DOB": self.DOB,
                "bookingID": self.bookingID, "addonsID": self.addonsID, "parentPassengerID": self.parentPassengerID, "membership_no": self.membership_no, "price": self.price, "seatNo": self.seatNo}


@app.route("/pass/addPassenger", methods=['POST'])
def addPassenger():
    data = request.get_json()
    passenger = Passenger(**data)
    print(passenger.json())

    try:
        db.session.add(passenger)
        db.session.commit()
    except Exception as inst:
        print(inst.args)
        return jsonify({"message": "An error occurred while adding the passenger."}), 500
    return jsonify(passenger.json()), 201


@app.route("/pass/passenger/<int:bookingID>")
def search_by_filter(bookingID):
    return jsonify({"passenger_info": [passenger_info.json() for passenger_info in Passenger.query.filter_by(bookingID=bookingID).all()]})


# @app.route("/pass/passenger", methods=['POST'])
# def receiveBooking():
#     # Check if the booking contains valid JSON
#     booking = None
#     if request.is_json:
#         booking = request.get_json()
#     else:
#         booking = request.get_data()
#         print("Received an invalid booking:")
#         print(booking)
#         replymessage = json.dumps(
#             {"message": "Booking should be in JSON", "data": booking}, default=str)
#         return replymessage, 400  # Bad Request

#     print("Received a booking by " + __file__)
#     result = processBooking(booking)
#     print()  # print a new line feed as a separator

#     # reply to the HTTP request
#     replymessage = json.dumps(result, default=str)
#     if result["status"]:
#         return replymessage, 200  # return the json along with the http status code 200
#     else:
#         return replymessage, 501  # return the json along with the http status code 501

# # For create booking & check in


# def processBooking(booking):
#     checkIn = True
#     print("Processing an booking:")
#     print(booking)
#     bookingID = booking['bookingID']  # 1
#     # print(bookingID)
#     parentPassengerID = booking['parentPassengerID']  # 50
#     passengerStr = ''

#     # Creation of booking
#     if(checkIn == False):
#         # Query the rows whereby parentpassengerID = e.g. 50
#         for row in Passenger.query.filter_by(parentPassengerID=parentPassengerID).all():
#             # print(row.passengerID)
#             # for each row, i want to take the passengerID as the primary key for the row as .get() must use primary key
#             primarykey = row.passengerID
#             item = Passenger.query.get(primarykey)
#             # then, i want to update the bookingID to 1^ for this passengerID so that it matches my parentpassenger's bookingID
#             item.bookingID = bookingID
#             db.session.commit()

#     # Check in
#     else:
#         for row in Passenger.query.filter_by(bookingID=bookingID).all():
#             primarykey = row.passengerID
#             item = Passenger.query.get(primarykey)  # item is a class

#             # print(item.passengerID) # to get value out of item class

#             passengerStr += str(item.passengerID) + ',' + item.name + ','

#         passengerStr = str(item.bookingID) + ':' + passengerStr
#         print(passengerStr)

#         passengerJson = json.dumps(passengerStr)
#         # print(passengerJson)
#         r = requests.post(bookingURL, json=passengerJson)

#         print("Passenger sent to booking.")

#         # return jsonify(booking.json()), 201

#     resultStatus = True
#     result = {'status': resultStatus}
#     if not resultStatus:  # inform the error handler when passenger fails
#         print("Failed passenger processing.")
#     else:
#         print("OK passenger processing.")
#     return result

# For cancellation of booking to delete passenger record
@app.route("/pass/passenger/<int:bookingID>", methods=['DELETE'])
def delete_booking(bookingID):
    exists = bool(Passenger.query.filter_by(bookingID=bookingID).first())
    if (not exists):
        return jsonify({"message": "Booking ID '{}' does not exist.".format(bookingID)}), 400

    try:
        Passenger.query.filter_by(bookingID=bookingID).delete()
        db.session.commit()

    except:
        return jsonify({"message": "An error occurred deleting the booking."}), 500

    return 'Booking has been removed', 201


@app.route("/pass/update_passenger/<int:passengerId>", methods=['PUT'])
def updatePassenger(passengerId):
    """
    This function updates a single booking using the given bookingID.
    For cancellation of booking to update isCancelled to True
    """
    if request.is_json:
        data = request.get_json()
    # exists = bool(Passenger.query.filter_by(parentPassengerID = passengerId).first())
    # if (exists == False):
    #     return jsonify({"message": "Passenger ID '{}' does not exist.".format(passengerId)}), 400
    print(passengerId)
    passenger = Passenger.query.filter_by(passengerID=passengerId).first()

    try:
        # (self, passportNo, name, email, DOB, bookingID, addonsID, parentPassengerID, membership_no, price, seatNo):
        passenger.name = data["name"]
        passenger.email = data["email"]
        passenger.seatNo = data["seatNo"]
        print(data["passportNo"])
        passenger.passportNo = data["passportNo"]
        passenger.addonsID = data["addonsID"]
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred updating the passenger."}), 500

    return jsonify({"message": 'Passenger has been updated'}), 201


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) +
          ": passenger for a booking...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
