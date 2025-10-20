# ☂️ Rain SMS Notifier (OpenWeather + Twilio)

Sends an SMS if rain is forecast in the next few hours at your coordinates.

## How it works
- Calls OpenWeather `forecast` API (`cnt=4` ≈ ~12 hours)
- If any weather code `< 700` appears, sends an SMS via Twilio
- Secrets/config are read from `.env`

## Setup
```bash
cp .env.example .env   # fill in your keys and numbers
pip install -r requirements.txt
python main.py

Environment variables

See .env.example for all required values.

Notes
	•	Uses request timeouts and an optional HTTPS proxy for Twilio.
	•	Prints friendly weather descriptions (e.g., 801 → Few clouds).

# 🛠 Tiny (optional) code touch
- Add units if you ever read temps later:
```python
weather_params = {"lat": MY_LAT, "lon": MY_LONG, "appid": api_key, "cnt": 4, "units": "metric"}
