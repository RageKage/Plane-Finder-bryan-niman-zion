import databaseManager
from databaseManager import *
from menu import Menu
import planeImage

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
    menu.add_option('3', 'Display Bookmarked Planes', display_bookmarked_planes)
    
    # menu.add_option('4', 'Bookmark a Plane', bookmark_plane) possible option, TBD whether this is worth it.
    
    menu.add_option('4', 'Delete Plane in DB', delete_bookmarked_plane)
    menu.add_option('5', 'Generate Test Data', create_sample_planes)
    menu.add_option('6', 'Exit Program', exit)

    return menu

def delete_bookmarked_plane(): # This is to delete a plane from the user db
    planes = db_manager.show_bookmarked_planes()
    for plane in planes:
        print(plane)
    delete = input('Enter plane model to delete:')
    db_manager.delete_plane_by_model_or_dbID(delete)
    pass

def search_aircraft_in_api(): # This is to search for the plane in the api
    search = input('Enter plane model to search:')
    image_url = planeImage.get_image_link(search)
    print(image_url)
    pass


def search_bookmarked_plane(): # this searches in the user db
    search = input('Enter the plane you want to search for (Model or icao): ')
    plane = db_manager.search_plane(search)
    if plane is None:
        print('Plane not found.')
    else:
        print(plane)

def add_plane_to_bookmarks(): # This is to add a plane to the user db
    pass


def display_bookmarked_planes(): # This displays all the planes in the user db
    planes = db_manager.show_bookmarked_planes()
    for plane in planes:
        print(plane)


# Developer test function just to create data to manipulate in the database. Should be removed once we can search for
# actual plane data.
def create_sample_planes():
    boeing = BookmarkedPlane(name='Boeing 737', description='a plane created by Boeing.')
    boeing.save()
    airbus = BookmarkedPlane(name='Airbus A-321neo', description='a plane created by Airbus.')
    airbus.save()


# Runs the program
if __name__ == '__main__':
    api_url = 'http://api.aviationstack.com/v1/airplanes'
    access_key = os.environ.get('AVIATIONS_API_KEY') # This is to get the api key from the environment variables
    
    if not os.path.exists('OneTimeMessage.txt'): # This is to check if the user has already been notified about the wait time for the api store the aircraft data into the db.
        
        print('')
        print('')
        print('Fetching all current data and populating it into database. This may take a while.')
        with open('OneTimeMessage.txt', 'w') as file:
            file.write('True') # This will create a file to indicate that the user has already been notified about the wait time for the api to store the aircraft data into the db.
    print('')   
    print('')
    db_manager = DatabaseManager(api_url, access_key) # This is to create the database manager object, with the api url and the access key.
    
    db_manager.setup_databases()  # This will set up your databases
    
    
    if not AircraftData.select().exists(): # This is to check if the aircraft data is already in the db. If it is then it won't fetch it again.
        db_manager.fetch_and_store_airplane_data() 
    Main()
