import databaseManager
from databaseManager import Plane
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
    menu.add_option('2', 'Search for a plane', plane_search)
    menu.add_option('3', 'Bookmark a plane', bookmark_plane)
    menu.add_option('4', 'Quit program', exit)
    menu.add_option('5', 'create test data', create_sample_planes)

    return menu


def plane_search():
    print('Currently nonfunctional')


def bookmark_plane():
    print('Currently nonfunctional')
    # To be added


# Shows all bookmarked planes
def show_bookmarked_planes():
    planes = databaseManager.get_planes()
    print()
    for plane in planes:
        print(plane)
    print()


# Developer test function just to create data to manipulate in the database. Should be removed once we can search for
# actual plane data.
def create_sample_planes():
    boeing = Plane(name='Boeing 737', description='a plane created by Boeing.')
    boeing.save()
    airbus = Plane(name='Airbus A-321neo', description='a plane created by Airbus.')
    airbus.save()


# Runs the program
if __name__ == '__main__':
    Main()