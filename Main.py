import databaseManager
from databaseManager import *
from menu import Menu

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
    menu.add_option('1', 'Show all bookmarked planes', show_bookmarked_planes)
    menu.add_option('2', 'Search for a plane in DB', plane_search)
    menu.add_option('3', 'Search for a plane in API', search_plane)
    # menu.add_option('3', 'Bookmark a plane', bookmark_plane) possible option, TBD whether this is worth it.
    menu.add_option('4', 'Quit program', exit)
    menu.add_option('5', 'create test data', create_sample_planes)

    return menu

def search_plane():
    search = input('Enter plane model to search:')
    pass


def plane_search():
    search = input('Enter the plane you want to search for (Model or icao): ')
    planes = UserPlane.select().where(UserPlane.model.contains(search) | UserPlane.icao.contains(search))
    for plane in planes:
        print(plane)

def bookmark_plane():
    pass


# Shows all bookmarked planes
def show_bookmarked_planes():
    planes = Plane.select()
    for plane in planes:
        print(plane)


# Developer test function just to create data to manipulate in the database. Should be removed once we can search for
# actual plane data.
def create_sample_planes():
    boeing = Plane(name='Boeing 737', description='a plane created by Boeing.')
    boeing.save()
    airbus = Plane(name='Airbus A-321neo', description='a plane created by Airbus.')
    airbus.save()


# Runs the program
if __name__ == '__main__':
    api_url = 'http://api.aviationstack.com/v1/airplanes'
    access_key = os.environ.get('AVIATIONS_API_KEY')
    
    if not os.path.exists('OneTimeMessage.txt'): # This is to check if the user has already been notified about the wait time for the api store the aircraft data into the db.
        
        print('')
        print('')
        print('Fetching all current data and populating it into database. This may take a while.')
        with open('OneTimeMessage.txt', 'w') as file:
            file.write('True') # This will create a file to indicate that the user has already been notified about the wait time for the api to store the aircraft data into the db.
    print('')   
    print('')
    db_manager = DatabaseManager(api_url, access_key)
    
    db_manager.setup_databases()  # This will set up your databases
    
    
    # Check if the database is empty
    if not UserPlane.select().exists() :
        db_manager.fetch_and_store_airplane_data() 
    Main()
