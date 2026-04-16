import requests
import joblib
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz
from supabase import create_client
import os
import time

model = joblib.load("rf_weather_model.pkl")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

WEATHER_API_KEY = "YOUR_OPENWEATHER_KEY"

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("yourgmail@gmail.com", "APP_PASSWORD")
        server.send_message(msg)

def predict_risk(temp, humidity, wind, clouds):
    hour = datetime.now().hour
    return model.predict([[temp, humidity, wind, clouds, hour]])[0]

while True:
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist).strftime("%H:%M")

    users = supabase.table("users").select("*").eq("alert_time", now).execute()

    for user in users.data:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={user['location']}&appid={WEATHER_API_KEY}&units=metric"
        ).json()

        temp = res["main"]["temp"]
        humidity = res["main"]["humidity"]
        wind = res["wind"]["speed"]
        clouds = res["clouds"]["all"]

        risk = predict_risk(temp, humidity, wind, clouds)

        if risk == "Warning":
            send_email(
                user["email"],
                "🚨 Weather Warning Alert",
                f"Severe weather predicted in {user['location']}. Please stay safe."
            )

    time.sleep(60)