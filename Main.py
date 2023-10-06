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


# Runs the program
if __name__ == '__main__':
    Main()