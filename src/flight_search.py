import requests
from flight_data import FlightData

TEQUILA_KEY = "" #Your Tequila API key
API_TEQUILA = "https://api.tequila.kiwi.com/locations/query" #The Tequila query API, used to find IATA codes for the airports of cities in the Google sheet where all the project data is kept.
FLIGHT_API = "https://api.tequila.kiwi.com/v2/search" #The Flight Search API, which uses data from the sheet to find flights.
HEADERS = {"apikey": TEQUILA_KEY,
           "Accept": "application/json"
}

class FlightSearch:

    #This class is responsible for talking to the Flight Search API.
    def insert_iata_codes(self, city):
        params = {'term': city}
        response = requests.get(url=API_TEQUILA, headers=HEADERS, params=params)
        response = response.json()
        return response["locations"][0]['code']
    
    def search_for_flight(self, fly_from, fly_to, date_from, date_to):
        nights_in_dst_from = 7
        nights_in_dst_to = 28
        curr = "GBP"
        params = {"fly_from": fly_from,
                  "fly_to": fly_to,
                  "date_from": date_from.strftime("%d/%m/%Y"),
                  "date_to": date_to.strftime("%d/%m/%Y"),
                  "nights_in_dst_from": nights_in_dst_from,
                  "nights_in_dst_to": nights_in_dst_to,
                  "curr": curr,
                  "max_stopovers": 0,
                  }
        response = requests.get(url=FLIGHT_API, headers=HEADERS, params=params)

        try:
            data = response.json()['data'][0]

        except IndexError:
                params["max_stopovers"] = 2
                data = response.json()['data'][0]
                response = requests.get(
                url=f"{FLIGHT_API}/v2/search",
                headers=HEADERS,
                params=params,
                )
                data = response.json()["data"][0]
                print(data)
                flight_data = FlightData(
                    price=data["price"],
                    departure_city=data["route"][0]["cityFrom"],
                    departure_iata=data["route"][0]["flyFrom"],
                    arrival_city=data["route"][1]["cityTo"],
                    arrival_iata=data["route"][1]["flyTo"],
                    outbound_date=data["route"][0]["local_departure"].split("T")[0],
                    inbound_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs= 1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
        
        else:
            print(f"{data['cityTo']}: {data['price']}£")
            price = data['price']
            city_from = data['route'][0]['cityFrom']
            from_iata = data['route'][0]['flyFrom']
            city_to = data['route'][0]['cityTo']
            to_iata = data['route'][0]['flyTo']
            outbound = data['route'][0]['local_departure'].split("T")[0]
            inbound = data['route'][1]['local_departure'].split("T")[0]
            flight_data = FlightData(price, city_from, from_iata, city_to, to_iata, outbound, inbound)
            return flight_data
        