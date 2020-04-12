Flight Scraper ✈️
Your one stop flight search engine 

**Can refer to README.md.html for easier reference**

Prerequisites
Please make your WAMP and RabbitMQ is not running (i.e port 80, 443, 8889 should be free)

Our application can be access via this URL: http://flightscraper.live/

Set Up Instructions
By default all the microservices will be running on cloud.

If there are any microservices that are not running you can follow the following instructions to start the service. 

List of Microservice App Name
- g8t2-runairline
- g8t2-booking 
- g8t2-init-flight-info 
- g8t2-notification 
- g8t2-passenger 
- g8t2-payment 
- g8t2-kong.herokuapp.com

If you are running windows, you can launch ubuntu and enter the following commands and run it in the shell.
Install heroku
- curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
If you are running MAC, you can launch the terminal and enter the following commands and run it in the shell. 
Install heroku
- brew tap heroku/brew && brew install heroku
    Follow the commands to restart the microservice
    1) cd docker/ {microservice_name}
    2) heroku login 
    *Refer to configuration file - if being prompt to enter credentials)
    3) heroku container: push web -a <app name>
    4) heroku container:release web -a <app name>

if KongAPI Gateway is not working:
heroku ps:restart web -a g8t2-kong

API Gateway URL
- g8t2-kong.herokuapp.com/runAirline/
- Booking - g8t2-kong.herokuapp.com/
- Passenger - g8t2-kong.herokuapp.com/pass
- Payment - g8t2-kong.herokuapp.com/payment

FlightScaper App
The application will be running on heroku cloud, there is no pre-configuration to be done. 

Do note that some features might not be available at all times as we are retrieving and processing external API. 
- If any instance the PayPal or SIA API are not working, just hit us up and we will show it via an online communication platform. 
- On any instance, where the PayPal sandbox run out of credits or it is not working you can visit this link and input this credentials (Email ID: sb-emf43r1154621@personal.example.com, System Generated Password: Ar/ju@5M)
- Due to the limitation call of the SIA API - you can toggle between this 2 keys (3aykdma5239dt43kqh8ecvsh, p9hucc924e383kdw9gd6bn9c) at docker/init_flightDB.py line 52

In term of demo, we would recommend using the following search criteria:
    Origin: Singapore
    Destination: Bangkok
    Departure Date: 20/03/2020
    Return Date: 14/04/2020
    *This is due to the limitations of the API call from SIA developer free tier account

Admin Panel
To access the admin panel: http://flightscraper.live/admin_login.html

Credentials
User: admin
Password: admin



















