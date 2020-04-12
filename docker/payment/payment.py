#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

"""
==================================
Step 1 : Import required packages.
==================================
"""
import json
import sys
import os
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import environ
import psycopg2

# Make sure to import this to make it easier to build your SQL queries
from sqlalchemy import text
# import requests

import paypalrestsdk
import pika

# Paypal configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "AUPQOeUEGSHaRxIhuMd96Z-5Lj9D1DWfdcbAKTR1JHvjEb-x8ZenqzBfOhRCzsCrYDq1K9G3vOMiqlS6",
    "client_secret": "EMVwkKSRrtFx0JBWSVCU-HicBX-4sOHgeN_JKNu0uxLDjbosqaTArXbtSmRnXCCT4AWLhi-JjrhwqOTr"
})
"""
=========================================================
Step 2 : Instantiate flask app and the SQLAlchemy object.
=========================================================
"""
app = Flask(__name__)

# Identify the location of the main database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/payment'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgres://ncvzzocqslkntg:92a856b0bc7f646c0fe4b2a0ea2c262ae74b438531db806b51fde72a1f481944@ec2-34-202-7-83.compute-1.amazonaws.com:5432/dfa8c2k69ng32h')


# So that warning message does not appear when I run the app - doing this will make warning message go away
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
CORS(app)


# bookingURL = "http://localhost:5002/booking"
# airlinesURL = "http://localhost:5001/airline"

"""
======================================================================
Step 3 : Create class that represent payment_info in Payment database.
======================================================================
"""


class Payment(db.Model):
    __tablename__ = 'payment_info'
    paymentID = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    bookingID = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    billing_address = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    name_on_card = db.Column(db.String, nullable=True)
    card_number = db.Column(db.String, nullable=True)
    exp_date = db.Column(db.String, nullable=True)
    cvv = db.Column(db.String, nullable=True)

    # sets the properties (of itself) when created

    def __init__(self, bookingID, email, billing_address, country, zip, total_cost, name_on_card, card_number, exp_date, cvv):
        self.bookingID = bookingID
        self.email = email
        self.billing_address = billing_address
        self.country = country
        self.zip = zip
        self.total_cost = total_cost
        self.name_on_card = name_on_card
        self.card_number = card_number
        self.exp_date = exp_date
        self.cvv = cvv

    # representation of data in json format
    def json(self):
        return {"paymentID": self.paymentID, "bookingID": self.bookingID, "email": self.email, "billing_address": self.billing_address, "country": self.country,
                "zip": self.zip, "total_cost": self.total_cost, "name_on_card": self.name_on_card, "card_number": self.card_number,
                "exp_date": self.exp_date, "cvv": self.cvv}


"""
=======================================================================
Step 5: paypal.html will come here to retrieve payment_info details
=======================================================================
"""


@app.route('/payment/pay/<int:total_flight_cost>', methods=['POST'])
# @app.route('/pay/', methods =['POST'])
def pay(total_flight_cost):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            # If Paypal fails then it should redirect back to the page at booking
            # Might need to change
            "return_url": "google.com",
            "cancel_url": "google.com"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Flight Booking",
                    "sku": 'item',
                    "price": float(total_flight_cost),
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": float(total_flight_cost),
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID': payment.id})


@app.route('/payment/execute_payment', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print('Execute Success!')
        success = True

    else:
        print(payment.error)

    return jsonify({'success': success})


@app.route("/payment/addpayment", methods=['POST'])
def addpayment():
    data = request.get_json()
    payment = Payment(**data)
    try:
        # print(data)
        # print(payment)
        db.session.add(payment)
        # print("Success")
        db.session.commit()
        print(payment.json())

        # Set up AMQP for passing to notification
        url = os.environ.get(
            'CLOUDAMQP_TEAL_URL', 'amqp://yhgwxorw:2TQl4jqQfFBYtLeHs-7RfWxJoNuDw47S@termite.rmq.cloudamqp.com/yhgwxorw')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        # Inserting AMQP here...
        # hostname = "localhost" # default hostname
        # port = 5672 # default port
        # connect to the broker and set up a communication channel in the connection
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
        channel = connection.channel()
        # set up the exchange if the exchange doesn't exist
        exchangename = "payment_direct"
        channel.exchange_declare(exchange=exchangename, exchange_type='direct')

        # convert the JSON object to a string
        resultmessage = json.dumps(payment.json(), default=str)

        print("result- " + resultmessage)
        # make sure the queue is bound to the exchange
        channel.queue_bind(exchange=exchangename,
                           queue='paymentHandler', routing_key='payment.status')
        channel.basic_publish(exchange=exchangename, routing_key="payment.status", body=resultmessage,
                              properties=pika.BasicProperties(delivery_mode=2))  # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        connection.close()

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while adding the payment information."}), 500
    return jsonify(payment.json()), 201


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5004, debug=True)
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port, debug=False)
