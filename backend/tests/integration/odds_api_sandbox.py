import requests
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("ODDS_API_HOST")
key = os.getenv("ODDS_API_KEY")
print("Host:", host, "Key:", key)

endpoint = "/v4/sports/basketball_nba/participants?apiKey=" + key

print("Endpoint:", host + endpoint)

response = requests.get(host + endpoint)
print("Response Status Code:", response.status_code)
print("Response Content:", response.content)

if response.status_code == 200:
    data = response.json()

    for team in data:
        print(f"Team Name: {team['full_name']}")
