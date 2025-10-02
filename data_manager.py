from flight_data import FlightData
import requests
import os

SHEETY_TOKEN = os.environ["SHEETY_FLIGHT_DEALS_TOKEN"]

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_url = "https://api.sheety.co/2b042b86b3141fb5eb68ec765b5f9d88/flightDeals/prices"
        self.sheety_header = {
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }

    def populate_iata_codes(self, iata_code, id):

        data = {
            "price": {
                "iataCode": iata_code
            }
        }
        sheety_response = requests.put(url=f"{self.sheety_url}/{id}", json=data, headers=self.sheety_header)
        print(sheety_response.text)

    def get_flight_deals_rows(self):
        sheety_response = requests.get(url=self.sheety_url, headers=self.sheety_header)
        flight_deals_rows = sheety_response.json()["prices"]
        flight_deals_rows = [FlightData(city=flight_deal["city"], iata_code=flight_deal["iataCode"], lowest_price=flight_deal["lowestPrice"], id=flight_deal["id"]) for flight_deal in flight_deals_rows]
        return flight_deals_rows

    def populate_lowest_price(self, lowest_price, flight_deal):
        data = {
            "price": {
                "lowestPrice": lowest_price
            }
        }

        sheety_response = requests.put(url=f"{self.sheety_url}/{flight_deal.id}", json=data,
                                       headers=self.sheety_header)
        print(sheety_response.text)

