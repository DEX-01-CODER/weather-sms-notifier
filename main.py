import os
import requests
from dotenv import load_dotenv
from twilio.http.http_client import TwilioHttpClient
from twilio.rest import Client

load_dotenv()

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.getenv("OWM_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TO_NUMBER = os.getenv("TO_NUMBER")
MY_LAT = float(os.getenv("MY_LAT", 0))
MY_LONG = float(os.getenv("MY_LONG", 0))
HTTPS_PROXY = os.getenv("HTTPS_PROXY")  # optional

# Basic validation to help catch missing configuration
required = {
    "OWM_API_KEY": api_key,
    "TWILIO_ACCOUNT_SID": account_sid,
    "TWILIO_AUTH_TOKEN": auth_token,
    "TWILIO_FROM": TWILIO_FROM,
    "TO_NUMBER": TO_NUMBER,
}
missing = [k for k, v in required.items() if not v]
if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=weather_params, timeout=10)
response.raise_for_status()
weather_data = response.json()
# Weather code descriptions (based on OpenWeatherMap condition codes)
weather_descriptions = {
    200: "Thunderstorm with light rain",
    201: "Thunderstorm with rain",
    202: "Thunderstorm with heavy rain",
    210: "Light thunderstorm",
    211: "Thunderstorm",
    212: "Heavy thunderstorm",
    221: "Ragged thunderstorm",
    230: "Thunderstorm with light drizzle",
    231: "Thunderstorm with drizzle",
    232: "Thunderstorm with heavy drizzle",
    300: "Light drizzle",
    301: "Drizzle",
    302: "Heavy drizzle",
    500: "Light rain",
    501: "Moderate rain",
    502: "Heavy rain",
    503: "Very heavy rain",
    504: "Extreme rain",
    511: "Freezing rain",
    520: "Light shower rain",
    521: "Shower rain",
    522: "Heavy shower rain",
    600: "Light snow",
    601: "Snow",
    602: "Heavy snow",
    611: "Sleet",
    612: "Light shower sleet",
    613: "Shower sleet",
    615: "Light rain and snow",
    616: "Rain and snow",
    620: "Light shower snow",
    621: "Shower snow",
    622: "Heavy shower snow",
    701: "Mist",
    711: "Smoke",
    721: "Haze",
    731: "Dust whirls",
    741: "Fog",
    751: "Sand",
    761: "Dust",
    762: "Volcanic ash",
    771: "Squalls",
    781: "Tornado",
    800: "Clear sky",
    801: "Few clouds",
    802: "Scattered clouds",
    803: "Broken clouds",
    804: "Overcast clouds",
}

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    description = weather_descriptions.get(int(condition_code), "Unknown condition")
    print(f"Weather ID {condition_code}: {description}")
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # Optional corporate proxy support
    if HTTPS_PROXY:
        proxy_client = TwilioHttpClient()
        proxy_client.session.proxies = {"https": HTTPS_PROXY} # type: ignore
        client = Client(account_sid, auth_token, http_client=proxy_client)
    else:
        client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_=TWILIO_FROM,
        to=TO_NUMBER, # type: ignore
    )
    print(message.status)

