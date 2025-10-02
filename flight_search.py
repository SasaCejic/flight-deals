import os
import requests
from data_manager import DataManager
from datetime import datetime,timedelta

AMADEUS_API_KEY = os.environ["AMADEUS_API_KEY"]
AMADEUS_API_SECRET = os.environ["AMADEUS_API_SECRET"]
DEPARTURE_CITY_CODE = "LON"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        self.amadeus_headers = {
            "Authorization": f"Bearer {self.get_access_token()}"

        }

    def get_access_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }

        response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token", data=payload, headers=headers)
        return response.json()["access_token"]

    def populate_iata_codes(self):
        dm = DataManager()
        flight_deals_rows = dm.get_flight_deals_rows()

        for flight_deal in flight_deals_rows:
            if not flight_deal["iataCode"].strip():
                amadeus_params = {
                    "keyword": flight_deal["city"]
                }
                amadeus_response = requests.get(url="https://test.api.amadeus.com/v1/reference-data/locations/cities", params=amadeus_params, headers=self.amadeus_headers)
                amadeus_response.raise_for_status()
                flight_deal["iataCode"] = amadeus_response.json()["data"][0]["iataCode"]
                dm.populate_iata_codes(amadeus_response.json()["data"][0]["iataCode"], flight_deal['id'])

    def find_cheapest_flights(self):
        amadeus_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

        tomorrow = datetime.now() + timedelta(days=1)
        six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

        dm = DataManager()
        flight_deals_rows = dm.get_flight_deals_rows()

        for flight_deal in flight_deals_rows:
            amadeus_params = {
                "originLocationCode": DEPARTURE_CITY_CODE,
                "destinationLocationCode": flight_deal.iata_code,
                "departureDate": tomorrow.strftime("%Y-%m-%d"),
                "returnDate": six_month_from_today.strftime("%Y-%m-%d"),
                "adults": 1,
                "nonStop": "true",
                "currencyCode": "GBP",
                "max": 10
            }

            amadeus_response = requests.get(url=amadeus_url, params=amadeus_params, headers=self.amadeus_headers)

            prices = []
            if len(amadeus_response.json()["data"]) > 0:
                for price in amadeus_response.json()["data"]:
                    print(flight_deal.iata_code)
                    print(price["price"]["total"])
                    prices.append(price["price"]["total"])

            prices = [float(price) for price in prices]

            if len(prices) > 0 and min(prices) < flight_deal.lowest_price:
                flight_deal.lowest_price = min(prices)
                dm.populate_lowest_price(flight_deal.lowest_price, flight_deal)
