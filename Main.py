import os
from databaseManager import *
from wiki_plane_info import *
from menu import Menu
import planeImage
from airport_cache import fetch_and_cache_airports, flight_info_with_airport_names
import ui
from planeModel import FlightInfo

# env variables
Airlabs_apiKey = os.environ.get('AIRLABS_API_KEY')
Aviation_apiKey = os.environ.get('AVIATIONS_API_KEY')


def Main():
    """This function creates the menu and displays the menu and gets the user input and runs the action."""
    menu = create_menu()
    while True:
        print(menu)
        choice = input('Enter action here: ')
        action = menu.get_choice(choice)
        if action == 'invalid':
            print('That was an invalid input. Please try again from the given options.')
        elif action == exit:
            print('Thanks for using Plane Finder!')
            exit()
        else:
            action()


def create_menu():
    """This is the main function that creates the menu and adds the options to the menu."""
    menu = Menu()
    menu.add_option('1', 'DB Plane Search', search_bookmarked_plane)
    menu.add_option('2', 'API Plane Search', search_aircraft_in_api)
    menu.add_option('3', 'Display Bookmarked Planes',
                    display_bookmarked_planes)
    menu.add_option('4', 'Delete Plane in DB', delete_bookmarked_plane)
    menu.add_option('5', 'Generate Test Data', create_sample_planes)
    menu.add_option('6', 'Exit Program', exit)
    return menu


def create_bookmark_menu():
    """This function creates the bookmark menu and adds the options to the menu."""
    menu = Menu()
    menu.add_option('1', 'Bookmark this plane', add_plane_to_bookmarks)
    menu.add_option('2', 'Go back to main menu', go_back)
    return menu


def delete_bookmarked_plane():
    """This function deletes a bookmarked plane from the database."""
    planes = db_manager.show_bookmarked_planes()
    for plane in planes:
        print(plane)
    delete = input('Enter plane model to delete:')
    db_manager.delete_plane_by_model(delete)


def search_aircraft_in_api():
    """This function searches for an aircraft in the api and displays the information about the aircraft."""

    user_input = input('Enter plane model or icao code to search:').strip()
    fetch_and_cache_airports(Airlabs_apiKey)
    if not user_input:
        print('Please enter a valid plane model or icao code.')
        return
    if len(user_input) <= 4:
        aircraft = db_manager.search_aircraft_by_icao(user_input)
        if not aircraft:
            print('Plane not found.')
            return
        else:
            search = aircraft
    else:
        models = db_manager.search_aircraft_by_model(user_input)
        if not models:
            print('Plane not found.')
            return
        else:
            if len(models) == 1:
                search = models[0]
            else:
                search = filter_through_aircrafts(models)
                if not search:
                    print('Plane not found.')
                    return

    "This is where the flight info is fetched "
    flight_info_obj = FlightInfo(Airlabs_apiKey, search.icao)
    flight_info_obj.fetch_flight_info()
    flights = flight_info_obj.get_filtered_flight_info()

    "This gets current flight info, image, and description"
    current_flights = flight_info_with_airport_names(flights)
    image_url = planeImage.get_image_link(search.model)
    description = PlaneInfo.clean_extract_text(
        PlaneInfo.extract_page_info(PlaneInfo.make_wikipedia_request(search.model)))

    "This displays the information about the aircraft and the current flights"
    ui.display_aircraft_info(description, search.model)
    ui.show_current_flights(current_flights)
    ui.show_image_url(image_url)

    "This is where the bookmark menu is created and the options are added to the menu."
    bookmark_menu = create_bookmark_menu()
    handle_bookmark_menu(bookmark_menu, search, description, image_url)


def handle_bookmark_menu(bookmark_menu, search, description, image_url):
    """This function handles the bookmark menu and displays the menu and gets the user input and runs the action."""
    while True:
        print(bookmark_menu)
        choice = input('Enter action here: ')
        action = bookmark_menu.get_choice(choice)
        if action is go_back:
            action()
            break
        elif action == 'invalid':
            print('That isn\'t a valid input please try again.')
        else:
            action(search.model, description, image_url)


def filter_through_aircrafts(aircrafts):
    """This function filters through all the aircraft and displays the aircraft and gets the user input and returns the
    aircraft that the user chose. Also, this function checks for duplicates and only displays one of each aircraft."""
    icao_codes = set()
    counter = 0
    for aircraft in aircrafts:
        if aircraft.icao not in icao_codes:
            counter += 1
            print(f"{counter}. {aircraft.model} - {aircraft.icao}")
            icao_codes.add(aircraft.icao)
    choice = input('Enter the ICAO to search: ')
    while choice not in icao_codes:
        print('Enter a valid ICAO code.')
        choice = input('Enter the ICAO to search: ')
    for aircraft in aircrafts:
        if aircraft.icao == choice:
            return aircraft
    return None


def search_bookmarked_plane():
    """This function searches for a bookmarked plane in the database and displays the information about the plane."""
    search = input('Enter the plane you want to search for by Model Name: ')
    plane = db_manager.search_plane(search)
    if plane is None:
        print('Plane not found.')
    else:
        print(plane)


def add_plane_to_bookmarks(name, description, url):
    """This function adds a plane to the database."""
    new_plane = BookmarkedPlane(
        name=name, description=description, image_url=url)
    new_plane.save()


def display_bookmarked_planes():
    """This function displays all the bookmarked planes in the database."""
    planes = db_manager.show_bookmarked_planes()
    ui.display_bookmarked_planes(planes)


def go_back():
    """This function sends the user back to the main menu."""
    print('\nOk, sending you back...\n')


def create_sample_planes():
    """THis function creates sample planes and adds them to the database."""
    boeing = BookmarkedPlane(
        name='Boeing 737', description='a plane created by Boeing.', image_url='fakelink.com')
    boeing.save()
    airbus = BookmarkedPlane(
        name='Airbus A-321neo', description='a plane created by Airbus.', image_url='fakelink2.com')
    airbus.save()


if __name__ == '__main__':
    """This is the main function that runs the program. This creates the db folder and also checks to see if the 
    OneTimeMessage.txt file exists and if it doesn't then it will fetch all the data from the api and populate the database."""
    api_url = 'http://api.aviationstack.com/v1/airplanes'
    if not os.path.exists('OneTimeMessage.txt'):
        print('Fetching all current data and populating it into database. This may take a while.')
        with open('OneTimeMessage.txt', 'w') as file:
            file.write('True')
    db_manager = DatabaseManager(api_url, Aviation_apiKey)
    db_manager.setup_databases()
    if not AircraftData.select().exists():
        db_manager.fetch_and_store_airplane_data()
    Main()
