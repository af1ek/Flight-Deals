import requests
SHEETY_API = "" #The link to the Sheety API
SHEETY_BEARER = "" #Your Sheety Bearer/password
headers = {
    'Authorization': f'Bearer {SHEETY_BEARER}',
    'Content-Type': 'application/json',
}
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
      self.destination_data = {}  

    def read_function(self):
        response = requests.get(SHEETY_API, headers=headers)
        data = response.json()
        print(data)
        return data['prices']
        
    def update_destination_codes(self):
       for city in self.destination_data:
        data = {"price": 
                {
                    'iataCode': city['iataCode']
                    }
                    }
        response = requests.put(url=f"{SHEETY_API}/{city['id']}", json=data, headers=headers)

data_manager = DataManager
data_manager.read_function(data_manager)
