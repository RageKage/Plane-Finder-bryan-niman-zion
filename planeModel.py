import requests

class FlightInfo:
    def __init__(self, api_key, icao_code): 
        self.api_key = api_key
        self.icao_code = icao_code
        self.flight_info_dict = {} # empty dictionary to store flight info
         
    def fetch_data_from_api(self): # fetch flight info from the api and return it only if it's 200 OK
        url = f"https://airlabs.co/api/v9/flights?api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return []

        
    def process_flight_data(self, data):
        plane_count = 0  # counter for the number of planes processed, their are just way too many planes to process
        for item in data: 
            aircraft_icao = item.get('aircraft_icao', '') # this will get the aircraft icao code
            dep_icao = item.get('dep_icao', '')
            arr_icao = item.get('arr_icao', '')

            if aircraft_icao == self.icao_code:
                unique_key = plane_count + 1  # This is the unique key for the dictionary
                self.flight_info_dict[unique_key] = {
                    "aircraft_icao": aircraft_icao,
                    'dep_icao': dep_icao,
                    'arr_icao': arr_icao,
                }
                plane_count += 1  # Increment the plane count
                if plane_count >= 5: # this will only process 5 planes
                    break 
        
    def fetch_flight_info(self):
        data = self.fetch_data_from_api()
        self.process_flight_data(data)

    def get_filtered_flight_info(self): 
        return self.flight_info_dict # Get the filtered flight info dictionary and return it
