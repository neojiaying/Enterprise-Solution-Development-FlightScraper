import requests
import mysql.connector
import json
from random import randint
import time
from datetime import datetime
import psycopg2
import schedule
# Set up DB configuration
# For windows port=3306 password=''
# For Mac port=8889 password='root'

conn = psycopg2.connect(
    host="ec2-35-174-88-65.compute-1.amazonaws.com",
    user="bfnyyievvpmzxo",
    password="f00e9a52b665e400420bdfd59bdb764ded194dcfe543a3a4a1cafc60aab0c8f4",
    database="dductjgrep939t",
    port=5432
)


mycursor = conn.cursor()


# # ------- Retrieving airline ID and Airline Name ---------
# # ****** RUN THIS PART ONCE (Comment out after you got the data) *******
# response = requests.get("http://api.aviationstack.com/v1/airlines?access_key=91081dd80924081b2832facd15ecb497")
# airline_info = response.json()
# for single_airline in airline_info['data']:
#     airline_name = single_airline['airline_name']
#     airline_id = single_airline['iata_code']
#     sql = "INSERT INTO airline_info (airlineID, airlineName) VALUES (%s, %s)"
#     val = (airline_id, airline_name)
#     mycursor.execute(sql, val)
#     mydb.commit()
# # End of retrieving airline id and airline name




# Get all Iata Code and put in an array
def run_script():
    mycursor.execute('SELECT "iataCode" FROM "airport_info";')
    iata_codes = mycursor.fetchall()
    today = datetime.today().strftime('%Y-%m-%d')
    for iata in iata_codes:
        for all_iata in iata_codes:
            if (all_iata != iata):
                origin = iata[0]
                destination = all_iata[0]
                url = "https://apigw.singaporeair.com/api/v1/commercial/flightavailability/get"
                data = {"request":{"itineraryDetails":[{"originAirportCode":origin, "destinationAirportCode":destination, "departureDate":"2020-03-31", "returnDate":"2020-04-14"}],"cabinClass":"Y", "adultCount":1, "childCount":0, "infantCount":0, "flightSortingRequired":False, "flexibleDates":False,  "dateRange":"1"}, "clientUUID":"TestIODocs"}
                headers = {"apikey": "3aykdma5239dt43kqh8ecvsh", "X-Originating-IP": "202.161.35.27", "Content-Type": "application/json"}
                response= requests.post(url,data=json.dumps(data), headers=headers)
                #key - p9hucc924e383kdw9gd6bn9c
                #key -
                try:
                    print("running")
                    airport_info = response.json()
                    print(airport_info)
                    responseinfo = airport_info["response"]
                    recommendationinfo = responseinfo["recommendations"][0]
                    segmentsdetail = recommendationinfo["segmentBounds"][0]
                    segments = segmentsdetail["segments"][0]
                    seatsLeft = segments["numOfLastSeats"]
                    price = segmentsdetail["fareSummary"]["fareTotal"]["totalAmount"]
                    flightsinfo = responseinfo["flights"][0]
                    flightNumber = flightsinfo["segments"][0]["legs"][0]["flightNumber"]
                    departureDateTime = flightsinfo["segments"][0]["legs"][0]["departureDateTime"]
                    flightDuration = flightsinfo["segments"][0]["tripDuration"]
                    airlineId = flightsinfo["segments"][0]["legs"][0]['operatingAirline']['code']
                    flightsinforeturn = responseinfo["flights"][1]
                    returnDateTime = flightsinforeturn["segments"][0]["legs"][0]["departureDateTime"]
                    sql = 'INSERT INTO "flight_info" ("flightNumber", "airlineId", "origin", "destination", "outbound", "inbound", "outbound_time", "inbound_time", "flightDuration", "seatsLeft", "price", "Class") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                    print(sql)
                    val = (flightNumber, 'SQ', origin, destination, departureDate, returnDate, departureDateTime, returnDateTime, flightDuration, seatsLeft, price, "Y")
                    print(val)
                    mycursor.execute(sql, val)
                    conn.commit()

                except:
                    print("No Flight to this area")


if __name__ == '__main__':
    run_script()

schedule.every(10).seconds.do(run_script)
schedule.every().day.do(run_script(today))
while 1:
    schedule.run_pending()
    time.sleep(1)
