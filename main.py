import os
import requests

AMADEUS_API_KEY = os.environ["AMADEUS_API_KEY"]
AMADEUS_API_SECRET = os.environ["AMADEUS_API_SECRET"]
AMADEUS_TOKEN = os.environ["AMADEUS_TOKEN"]

amadeus_url = "https://test.api.amadeus.com/v1/shopping/flight-destinations"

amadeus_headers = {
    "Authorization": f"Bearer {AMADEUS_TOKEN}"

}
amadeus_params = {
    "origin": "PAR",
    "maxPrice": 200
}

response = requests.get(url=amadeus_url, params=amadeus_params, headers=amadeus_headers)

print(response.text)