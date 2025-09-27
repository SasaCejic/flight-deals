import os
import requests

AMADEUS_API_KEY = os.environ["AMADEUS_API_KEY"]
AMADEUS_API_SECRET = os.environ["AMADEUS_API_SECRET"]
AMADEUS_TOKEN = os.environ["AMADEUS_TOKEN"]
SHEETY_TOKEN = os.environ["SHEETY_FLIGHT_DEALS_TOKEN"]

# REQUESTING 30-MIN ACCESS TOKEN (before first Amadeus API call)
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
# }
#
# payload = {
#     "grant_type": "client_credentials",
#     "client_id": AMADEUS_API_KEY,
#     "client_secret": AMADEUS_API_SECRET
# }
#
# response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token", data=payload, headers=headers)
# print(response.text)


# GET CITY IATA CODE BY CITY NAME

# amadeus_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
#
# amadeus_headers = {
#     "Authorization": f"Bearer {AMADEUS_TOKEN}"
#
# }
# amadeus_params = {
#     "keyword": "New York"
# }
#
# amadeus_response = requests.get(url=amadeus_url, params=amadeus_params, headers=amadeus_headers)
#
# print(amadeus_response.json()["data"][0]["iataCode"])


# GETTING ALL ROWS FROM MY SPREADSHEET

sheety_url = "https://api.sheety.co/2b042b86b3141fb5eb68ec765b5f9d88/flightDeals/prices"

sheety_header = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

sheety_response = requests.get(url=sheety_url, headers=sheety_header)
flight_deals_rows = sheety_response.json()["prices"]

# {
#     'city': 'Paris',
#     'iataCode': '',
#     'lowestPrice': 54,
#     'id': 2
# }


# FILL IN IATA CODES IF EMPTY IN GOOLGLE SHEET

amadeus_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

amadeus_headers = {
    "Authorization": f"Bearer {AMADEUS_TOKEN}"

}

for flight_deal in flight_deals_rows:
    if not flight_deal["iataCode"].strip():
        amadeus_params = {
            "keyword": flight_deal["city"]
        }
        amadeus_response = requests.get(url=amadeus_url, params=amadeus_params, headers=amadeus_headers)
        amadeus_response.raise_for_status()
        flight_deal["iataCode"] = amadeus_response.json()["data"][0]["iataCode"]

        data = {
            "price": {
                "iataCode": flight_deal["iataCode"]
            }
        }


        sheety_response = requests.put(url=f"{sheety_url}/{flight_deal['id']}", json=data, headers=sheety_header)
        print(sheety_response.text)

# google sheet link: https://docs.google.com/spreadsheets/d/1GduhLn1O2Miulm1-1li-SN38bvraBrUb0XjKkwUaenA/edit?gid=0#gid=0