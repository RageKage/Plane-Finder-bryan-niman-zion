import requests

class FlightInfo:
    """This class will fetch the flight info from the api and store it into a dictionary."""
    def __init__(self, api_key, icao_code):
        self.api_key = api_key
        self.icao_code = icao_code
        self.flight_info_dict = {}

    def fetch_data_from_api(self):
        """This will fetch the data from the api and return it as an object."""
        url = f"https://airlabs.co/api/v9/flights?api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return []

    def process_flight_data(self, data):
        """This will process the flight data and store it into a dictionary."""
        plane_count = 0
        for item in data:
            aircraft_icao = item.get('aircraft_icao', '')
            dep_icao = item.get('dep_icao', '')
            arr_icao = item.get('arr_icao', '')
            if aircraft_icao == self.icao_code:
                unique_key = plane_count + 1
                self.flight_info_dict[unique_key] = {
                    "aircraft_icao": aircraft_icao,
                    'dep_icao': dep_icao,
                    'arr_icao': arr_icao,
                }
                plane_count += 1
                if plane_count >= 5:
                    break

    def fetch_flight_info(self):
        data = self.fetch_data_from_api()
        self.process_flight_data(data)

    def get_filtered_flight_info(self):
        """This function returns the filtered flight info."""
        return self.flight_info_dict
