FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./flightInfo.py .
COPY ./airportInfo.py .
COPY ./runAirline.py .
CMD [ "python", "./runAirline.py" ]