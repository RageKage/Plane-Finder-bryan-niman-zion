import databaseManager
from databaseManager import *
from menu import Menu
import planeImage
from airport_cache import fetch_and_cache_airports, flight_info_with_airport_names


from planeModel import FlightInfo

# env variables
Airlabs_apiKey = os.environ.get('AIRLABS_API_KEY')
Aviation_apiKey = os.environ.get('AVIATIONS_API_KEY')


def Main():

    # Create a menu here.
    menu = create_menu()

    while True:
        print(menu)
        choice = input('Enter action here: ')
        action = menu.get_choice(choice)
        if action is None:
            exit()
        action()


# this function creates the menu to be seen by the user.
def create_menu():
    menu = Menu()
    menu.add_option('1', 'DB Plane Search', search_bookmarked_plane)
    menu.add_option('2', 'API Plane Search', search_aircraft_in_api)
    menu.add_option('3', 'Display Bookmarked Planes',
                    display_bookmarked_planes)

    # menu.add_option('4', 'Bookmark a Plane', bookmark_plane) possible option, TBD whether this is worth it.

    menu.add_option('4', 'Delete Plane in DB', delete_bookmarked_plane)
    menu.add_option('5', 'Generate Test Data', create_sample_planes)
    menu.add_option('6', 'Exit Program', exit)

    return menu


# Adds 2 options to a menu after each time the user searches for a plane.
def create_bookmark_menu():
    menu = Menu()
    menu.add_option('1', 'Bookmark this plane', add_plane_to_bookmarks)
    menu.add_option('2', 'Go back to main menu', go_back)

    return menu


def delete_bookmarked_plane():  # This is to delete a plane from the user db
    planes = db_manager.show_bookmarked_planes()
    for plane in planes:
        print(plane)
    delete = input('Enter plane model to delete:')
    db_manager.delete_plane_by_model_or_dbID(delete)
    pass


"""This function is called when a user wants to find out more information about a specific plane model. So far the user
   can get a url to an image of the plane they searched for by calling the Flickr API. TBA calls that will also get the
   current number of that model flying, and a description of the plane. These will be displayed together."""


def search_aircraft_in_api():
    # TODO make cure that it isn't case sensitive
    # TODO maybe create another .py but to just show the user instead of having prints in the main.py
    # TODO now we have the api working merge the codes so it works as intended
    user_input = input('Enter plane model or icao code to search:').strip()
    fetch_and_cache_airports(Airlabs_apiKey)

    # Return if no input is provided
    if not user_input:
        print('Please enter a valid plane model or icao code.')
        return

    # If user input is an ICAO code
    if len(user_input) <= 4:  # the format of a icao is that it must be less then 4 characters
        aircraft = db_manager.search_aircraft_by_icao(user_input)
        if not aircraft:
            print('Plane not found.')
            return
        else:
            search = aircraft

 # this is when they but in something that isn't an icao code like model name
    else:
        models = db_manager.search_aircraft_by_model(user_input)
        if not models:
            print('Plane not found.')
            return
        else:
            if len(models) == 1:  # if there is only one model then it will just return that model
                search = models[0]
            else:
                # if there is more then one model then it will filter through them and return the one they chose
                search = filter_through_aircrafts(models)

    flight_info_obj = FlightInfo(Airlabs_apiKey, search.icao)
    flight_info_obj.fetch_flight_info()
    # this will return a dictionary of the flight info with the icao codes and airport icao codes
    flights = flight_info_obj.get_filtered_flight_info()

    # this will return a list of the current flights with the airport names
    current_flights = flight_info_with_airport_names(flights)

    print(search)

    image_url = planeImage.get_image_link(search)

    print(image_url)  # This line should be removed/altered once all APIs are functional.

    description = 'test description'  # Stand-in for the wiki API.

    # Creates a menu with the option to bookmark a plane.
    bookmark_menu = create_bookmark_menu()

    # Loop pulled from Main(). Shows the bookmark_menu to choose options from.
    while True:
        print(bookmark_menu)
        choice = input('Enter action here: ')
        action = bookmark_menu.get_choice(choice)
        if action is go_back:
            action()
            break
        # Since there is only two actions, the second choice can have parameters already filled out.
        action(search, description, image_url)


# this just returns the aircraft model like list of them all

# this func will search the list of aircrafts and filter out the duplicates that are in the list
def filter_through_aircrafts(aircrafts):
    icao_codes = set()  # this is to store the icao codes so we don't have duplicates
    counter = 0  # this is to count the number of aircrafts

    for aircraft in aircrafts:
        if aircraft.icao not in icao_codes:
            counter += 1
            print(f"{counter}. {aircraft.model} - {aircraft.icao}")
            icao_codes.add(aircraft.icao)

    choice = input('Enter the ICAO to search: ')

    while choice not in icao_codes:  # this will check to see if the icao code is in the set
        print('Enter a valid ICAO code.')
        choice = input('Enter the ICAO to search: ')

    for aircraft in aircrafts:
        if aircraft.icao == choice:
            return aircraft.icao  # this will return the aircraft that the user chose

    return None


def search_bookmarked_plane():  # this searches in the user db
    search = input('Enter the plane you want to search for (Model or icao): ')
    plane = db_manager.search_plane(search)
    if plane is None:
        print('Plane not found.')
    else:
        print(plane)


"""This adds the recently searched plane to the 'bookmarked_planes' database. It requires a name, description, and image
   link of the plane to work."""


def add_plane_to_bookmarks(name, description, url):
    new_plane = BookmarkedPlane(
        name=name, description=description, image_url=url)
    new_plane.save()


def display_bookmarked_planes():  # This displays all the planes in the user db
    planes = db_manager.show_bookmarked_planes()
    for plane in planes:
        print(plane)


def go_back():  # Very short function since the menu object requires a function parameter. This is just to give the user
    # a response before pulling up the main menu.
    print('\nOk, sending you back...\n')


# Developer test function just to create data to manipulate in the database. Should be removed once we can search for
# actual plane data.
def create_sample_planes():
    boeing = BookmarkedPlane(
        name='Boeing 737', description='a plane created by Boeing.', image_url='fakelink.com')
    boeing.save()
    airbus = BookmarkedPlane(
        name='Airbus A-321neo', description='a plane created by Airbus.', image_url='fakelink2.com')
    airbus.save()


# Runs the program
if __name__ == '__main__':
    api_url = 'http://api.aviationstack.com/v1/airplanes'
    # This is to get the api key from the environment variables

    # This is to check if the user has already been notified about the wait time for the api store the aircraft data into the db.
    if not os.path.exists('OneTimeMessage.txt'):

        print('')
        print('')
        print('Fetching all current data and populating it into database. This may take a while.')
        with open('OneTimeMessage.txt', 'w') as file:
            # This will create a file to indicate that the user has already been notified about the wait time for the api to store the aircraft data into the db.
            file.write('True')
    print('')
    print('')
    # This is to create the database manager object, with the api url and the access key.
    db_manager = DatabaseManager(api_url, Aviation_apiKey)

    db_manager.setup_databases()  # This will set up your databases

    # This is to check if the aircraft data is already in the db. If it is then it won't fetch it again.
    if not AircraftData.select().exists():
        db_manager.fetch_and_store_airplane_data()
    Main()
