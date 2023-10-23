import requests

# Use a dictionary to cache the airport names
airport_cache = {}

def fetch_and_cache_airports(api_key):
    """Fetch airport data and cache it"""
    url = f"https://airlabs.co/api/v9/airports?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for airport in data.get('response', []):  # Default to empty list if 'response' not found
            airport_cache[airport['icao_code']] = airport['name']

def flight_info_with_airport_names(flight_info_dict):
    """Update flight info dict with names of dep_icao and arr_icao based on cached airport data"""
    for _, flight_info in flight_info_dict.items():
        flight_info['dep_airport'] = airport_cache.get(flight_info['dep_icao'], "Unknown Airport")
        flight_info['arr_airport'] = airport_cache.get(flight_info['arr_icao'], "Unknown Airport")
    return flight_info_dict
