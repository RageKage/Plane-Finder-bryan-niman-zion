def show_current_flights(current_flights):
    """Display the current flights."""
    banner()
    print('Current Flights:')
    print('')
    print('-' * len('Current Flights:'))
    for index, flights in current_flights.items():
        flight = flights  # Access the inner dictionary containing flight info
        print(f"Flight {flight['aircraft_icao']}: From {flight['dep_airport']} to {flight['arr_airport']}")
        

def display_aircraft_info(description, title):
    """Display the aircraft info."""
    banner()
    print('')
    print(f"{title}:")
    print('')
    print('-' * len(title)) 
    print(description)
    
    
def display_bookmarked_planes(planes):
    """Display the bookmarked planes."""
    print('Bookmarked Planes:\n')
    for plane in planes:
        print(f'ID: {plane.id}')

        print(f'Name: {plane.name}')
        
        print(f'Description: {plane.description}')

        print('')
        print(f'Image URL: {plane.image_url}')
        banner()
        print('')
        
def show_image_url(image_url):
    """Display the image url."""
    banner()
    print('')
    print(f'Image URL: {image_url}')
    banner()
    print('')
    
    

def banner():
    print('___' * 40)
    print('')
    
    