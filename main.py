import os
import requests
from datetime import datetime
import smtplib
from dotenv import load_dotenv
import time
load_dotenv()

MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

MY_LAT = 28.704060  # Your latitude
MY_LONG = 77.102493  # Your longitude


# Checks if your position is within +5 or -5 degrees of the ISS position.
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return abs(iss_latitude - MY_LAT) <= 5 and abs(iss_longitude - MY_LONG) <= 5


# Check if it is dark or not
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 5) % 24
    sunset = (int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 5) % 24

    time_now = datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="rajkhanna512@yahoo.com",
            msg="Subject:Look Up ☝️\n\nThe ISS is above you in the sky."
        )
