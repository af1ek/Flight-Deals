from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
import datetime

TODAY = datetime.date.today()
delta = datetime.timedelta(days=6*30)
TO_DATE = TODAY + delta

flight_search = FlightSearch()

CITY_FROM_IATA = "LON"

data_manager = DataManager()
sheet_data = DataManager().read_function()

if sheet_data[0]['iataCode'] == '':
    for row in sheet_data:
        row['iataCode'] = flight_search.insert_iata_codes(row['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

destinations = {
    data["iataCode"]: {
        "id": data["id"],
        "city": data["city"],
        "price": data["lowestPrice"]
    } for data in sheet_data}
notification_manager = NotificationManager()


# Flight search #
for destination_code in destinations:
    current_flight = flight_search.search_for_flight(CITY_FROM_IATA, destination_code, TODAY, TO_DATE)
    if current_flight == None:
        continue

    if current_flight != None and current_flight.price < destinations[destination_code]['price']:
        # print(f"This flight is cheaper for: {destinations[destination_code]['price'] - current_flight.price}")
        message = f"Cheap flight! Only £{current_flight.price} to fly from {current_flight.departure_city}-{current_flight.departure_iata} to {current_flight.arrival_city}-{current_flight.arrival_iata}, from {current_flight.outbound_date} to {current_flight.inbound_date}."
        
        if current_flight.stop_overs > 0:
            message += f"\nFlight has {current_flight.stop_overs} stop over, via {current_flight.via_city}."

        notification_manager.send_message(message)