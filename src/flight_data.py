class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, departure_city, departure_iata, arrival_city, arrival_iata, outbound, inbound, stop_overs=0, via_city=""):
        self.price = price
        self.departure_city = departure_city
        self.departure_iata = departure_iata
        self.arrival_city = arrival_city
        self.arrival_iata = arrival_iata
        self.outbound_date = outbound
        self.inbound_date = inbound
        self.stop_overs = stop_overs
        self.via_city = via_city