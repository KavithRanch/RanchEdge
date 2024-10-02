from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
odds_api_key = os.getenv('ODDS_API_KEY')


