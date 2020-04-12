from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from sqlalchemy import text
from datetime import date

import os
import requests
import json
import psycopg2

from os import environ

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:8889/booking"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/booking'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://eyjdkcblbphjoe:666f7a9675b82aa5e1c7ae68f45bb0686310d60e388f1d3f8092ada235fc84b0@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d3m3hieu35kclr')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# passengerURL = "https://g8t2-passenger.herokuapp.com/passenger"

db = SQLAlchemy(app)
CORS(app)


class Booking(db.Model):
    __tablename__ = "booking_info"

    # mirrors the existing booking info table
    # remember to update here if the columns are changed in DB !!

    bookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer())
    airlineID = db.Column(db.String())
    flightID = db.Column(db.String())
    parentPassengerID = db.Column(db.Integer())
    isCancelled = db.Column(db.Boolean)
    date = db.Column(db.Date())
    # numPassengers = db.Column(db.Integer())
    # sets the properties (of itself) when created

    # def __init__ (self, userID,airlineID,flightID, parentPassengerID,isCancelled, date, numPassengers):
    def __init__(self, userID, airlineID, flightID, parentPassengerID, isCancelled, date):
        self.userID = userID
        self.airlineID = airlineID
        self.flightID = flightID
        self.parentPassengerID = parentPassengerID
        self.isCancelled = isCancelled
        self.date = date
        # self.numPassengers = numPassengers

    # representation of data in json format

    def json(self):
        # return {"bookingID": self.bookingID, "userID": self.userID, "airlineID": self.airlineID,
        # "flightID": self.flightID, "parentPassengerID": self.parentPassengerID, "isCancelled": self.isCancelled, "date": self.date, "numPassengers": self.numPassengers}
        return {"bookingID": self.bookingID, "userID": self.userID, "airlineID": self.airlineID,
                "flightID": self.flightID, "parentPassengerID": self.parentPassengerID, "isCancelled": self.isCancelled, "date": self.date}


@app.route("/all_bookings")
def get_all():
    return jsonify({"bookings": [booking.json() for booking in Booking.query.all()]})


@app.route("/user_booking/<int:userID>")
def get_user_bookings(userID):
    """

    """
    return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(userID=userID).all()]})


@app.route("/booking/<int:bookingID>")
def get_one_booking(bookingID):
    """
    This function retrieves ONE booking from the booking_info table
    """
    try:
        return jsonify(Booking.query.filter_by(bookingID=bookingID).first().json())
    except:
        return jsonify({"message": "Booking not found."}), 404


@app.route("/flight_booking/<string:flightID>")
def get_flight_bookings(flightID):
    return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(flightID=flightID).all()]})


# @app.route("/parent_passenger_booking/<int:parentPassengerID>", methods=['GET'])
# def getbookingIDbyParentPassengerID(parentPassengerID):
#     """
#         For creation of booking & checking in: to match fields
#         Booking sending over parentPassengerID to passenger
#     """
#     # assume that a parentPassenger only has a booking
#     booking = Booking.query.filter_by(
#         parentPassengerID=parentPassengerID).first()
#     if booking:
#         r = requests.post(passengerURL, json=booking.json())
#         print(booking, "sent to passenger.")
#         return jsonify(booking.json()), 201

#     return jsonify({"message": "Booking not found."}), 404


@app.route("/update_booking/<int:bookingID>", methods=['PUT'])
def update_booking(bookingID):
    """
    This function updates a single booking using the given bookingID.
    For cancellation of booking to update isCancelled to True
    """
    exists = bool(Booking.query.filter_by(bookingID=bookingID).first())
    if (exists == False):
        return jsonify({"message": "Booking ID '{}' does not exist.".format(bookingID)}), 400

    try:
        for row in Booking.query.filter_by(bookingID=bookingID).all():
            primarykey = row.bookingID
            item = Booking.query.get(primarykey)
            item.isCancelled = True
            db.session.commit()
    except:
        return jsonify({"message": "An error occurred updating the booking."}), 500

    return 'Booking has been updated', 201


@app.route("/check_in_booking", methods=['POST'])
def receivePassenger():
    """

    """
    # Check if the booking contains valid JSON
    passenger = None
    passengerBookingInfo = ''

    if request.is_json:
        passenger = request.get_json()

        # To get int bookingID
        split = passenger.split(":")
        bookingID = split[0]
        bookingID = bookingID[1:]
        bookingID = int(bookingID)
        # print(bookingID)
        # print(type(bookingID)) #int

        passenger = passenger[1:-1]  # remove ""

        for row in Booking.query.filter_by(bookingID=bookingID).all():
            primarykey = row.bookingID
            item = Booking.query.get(primarykey)  # item is a class

            # print(item.passengerID) # to get value out of item class

            passengerBookingInfo += passenger + str(item.flightID) + ','
            passengerBookingInfo = passengerBookingInfo[:-1]
        print(passengerBookingInfo)  # string

    else:
        passenger = request.get_data()
        print("Received an invalid passenger:")
        print(passenger)
        replymessage = json.dumps(
            {"message": "Passenger should be in JSON", "data": passenger}, default=str)
        return replymessage, 400  # Bad Request

    print("Received a passenger by " + __file__)
    result = processPassenger(passenger)

    print()  # print a new line feed as a separator

    # reply to the HTTP request
    replymessage = json.dumps(result, default=str)
    if result["status"]:
        return replymessage, 200  # return the json along with the http status code 200
    else:
        return replymessage, 501  # return the json along with the http status code 501


def processPassenger(passenger):
    """
        This is a helper function for receivePassenger()
        app.route --> /check_in_booking

    """
    print("Processing a passenger:")
    # print(passenger)

    resultStatus = True
    result = {'status': resultStatus}
    if not resultStatus:  # inform the error handler when passenger fails
        print("Failed passenger processing.")
    else:
        print("OK passenger processing.")
    return result


@app.route("/add_booking", methods=["POST"])
def add_booking():
    data = request.get_json()
    print("asdadsad" + str(data))

    booking = Booking(**data, date=date.today())
    try:
        db.session.add(booking)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred creating the book."}), 500
    return jsonify(booking.json()), 201


'''For airline dashboard - Total number of bookings'''
@app.route("/num_bookings")
def get_num_bookings():
    num_bookings = Booking.query.count()
    return jsonify({"num_bookings": [num_bookings]})


'''For airline dashboard - Most Booked Flights'''
@app.route("/most_booked_flights")
def get_most_booked_flights():
    booked_flights = Booking.query.with_entities(Booking.flightID, func.count(
        Booking.flightID)).group_by(Booking.flightID).all()

    most_booked = max(booked_flights, key=lambda x: x[1])

    airlineURL = "https://g8t2-kong.herokuapp.com/runAirline/get_one_flight/" + \
        str(most_booked[0])

    r = requests.get(airlineURL)
    result = json.loads(r.text.lower())
    print(result)
    try:
        flightnumber = result['flightnumber']
        airlineid = result['airlineid']
        bookdetail = airlineid.upper() + " " + flightnumber
        return jsonify({"most_booked_flights": [bookdetail]}), 200
    except:
        return jsonify({"message": "Unable to get booking details"}), 500


'''For airline dashboard - Total Cancellations'''
@app.route("/total_cancellations")
def get_total_cancellations():
    total_cancellations = Booking.query.with_entities(Booking.isCancelled, func.count(
        Booking.isCancelled)).filter_by(isCancelled=True).group_by(Booking.isCancelled).all()
    if len(total_cancellations) == 0:
        return jsonify({"message": "No cancellations"}), 500
    return jsonify({"total_cancellations": [total_cancellations[0][1]]}), 200


'''For airline dashboard - Total Non-cancellations'''
@app.route("/total_non_cancellations")
def get_total_non_cancellations():
    total_non_cancellations = Booking.query.with_entities(Booking.isCancelled, func.count(
        Booking.isCancelled)).filter_by(isCancelled=False).group_by(Booking.isCancelled).all()
    print(total_non_cancellations)
    if len(total_non_cancellations) == 0:
        return jsonify({"message": "No bookings."}), 500
    return jsonify({"total_non_cancellations": [total_non_cancellations[0][1]]})


'''For airline dashboard - Booking Month'''
@app.route("/booking_month")
def get_booking_month():
    month_count = db.session.query(func.extract("month", Booking.date), func.count(
        Booking.date)).group_by(Booking.date).distinct(Booking.date).all()
    month_count_result = {}
    for month, count in month_count:
        if month not in month_count_result.keys():
            month_count_result[month] = count
        else:
            month_count_result[month] += count

    result = []
    months = list(month_count_result.keys())
    months.sort()

    for month in range(1, 13):
        if(month in month_count_result.keys()):
            result.append((int(month), month_count_result[month]))
        else:
            result.append((month, 0))
    print(result)
    return jsonify({"month_count": result})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
