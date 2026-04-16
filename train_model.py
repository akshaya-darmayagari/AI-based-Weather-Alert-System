import requests
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

WEATHER_API_KEY = "6f52153195a7db5e7301ebacc675093f"

cities = [
    "Hyderabad",
    "Delhi",
    "Mumbai",
    "Chennai",
    "Bangalore",
    "Kolkata"
]

data = []

for city in cities:
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != "200":
        continue

    for item in response["list"]:
        temp = item["main"]["temp"]
        humidity = item["main"]["humidity"]
        pressure = item["main"]["pressure"]
        wind_speed = item["wind"]["speed"]

        # RULE-BASED LABEL (for training only)
        if temp > 40 or temp<15 or humidity > 85:
            risk = 2   # Warning
        elif temp > 35:
            risk = 1   # Risky
        else:
            risk = 0   # Normal

        data.append({
            "temp": temp,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "risk": risk
        })

df = pd.DataFrame(data)

X = df[["temp", "humidity", "pressure", "wind_speed"]]
y = df["risk"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

joblib.dump(model, "weather_model.pkl")

print("✅ Random Forest model trained and saved as weather_model.pkl")