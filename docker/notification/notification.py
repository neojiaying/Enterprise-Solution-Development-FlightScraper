import json
import sys
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header


# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika


def receivePaymentLog():
    url = os.environ.get(
        'CLOUDAMQP_TEAL_URL', 'amqp://yhgwxorw:2TQl4jqQfFBYtLeHs-7RfWxJoNuDw47S@termite.rmq.cloudamqp.com/yhgwxorw')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    # hostname = "localhost" # default host
    # port = 5672 # default port
    # connect to the broker and set up a communication channel in the connection
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename = "payment_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare a queue for receiving messages
    # '' indicates a random unique queue name; 'exclusive' indicates the queue is used only by this receiver and will be deleted if the receiver disconnects.
    channelqueue = channel.queue_declare(queue='paymentHandler')
    # If no need durability of the messages, no need durable queues, and can use such temp random queues.
    queue_name = channelqueue.method.queue
    # bind the queue to the exchange via the key
    channel.queue_bind(exchange=exchangename, queue=queue_name,
                       routing_key='payment.status')
    # Can bind the same queue to the same exchange via different keys

    # set up a consumer and start to wait for coming messages
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    channel.start_consuming()  # start consuming (blocks)
    # connection.close()


# required signature for the callback; no return
def callback(channel, method, properties, body):
    print("Received a payment by " + __file__)
    print(json.loads(body))
    sendMail(json.loads(body))
    print()  # print a new line feed


def sendMail(payment_details):
    print(payment_details)
    email = payment_details["email"]
    fare = payment_details["total_cost"]
    booking_id = payment_details["bookingID"]

    try:
        # ------
        # create message object instance
        msg = MIMEMultipart()
        username = "flightscraper123@gmail.com"
        password = "fdsa4321"

        message = """
        <html>
            <head>
             <meta charset='utf-8'>
            </head>
            <body>

                    <h1>FlightScraper Payment Confirmation</h1>
                    <h3>Booking status: <strong>Confirmed</strong></h3>
                    <p>Dear Valued Customer,</p>
                    <p>We have received a payment of <u>$""" + str(fare) + """</u> from you for your booking <u>#""" + str(booking_id) + """</u>.</p>
                    <p>Best wishes,</p>
                    <p>FlightScraper &#128521;</p>
                
                <img src="https://wallpaperaccess.com/full/436417.jpg"  width="400" height="300">
            </body>
        </html>
            """

        # setup the parameters of the message
        msg['From'] = formataddr(
            (str(Header('FlightScraper', 'utf-8')), 'flightscraper123@gmail.com'))
        msg['To'] = email
        msg['Subject'] = "Confirmation Of Payment"

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(username, password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        print("successfully sent email to %s:", (msg['To']))
    except Exception as error:
        print(error)


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) +
          ": monitoring order creation...")
    receivePaymentLog()
