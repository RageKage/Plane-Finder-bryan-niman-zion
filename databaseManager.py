from peewee import *
import os
import requests

# This is the database for the user's planes.
bookmark_db_path = os.path.join('database', 'bookmarked_planes.sqlite')
aircraft_data_db_path = os.path.join('database', 'aircraft_data.sqlite')

bookmarkedPlaneDB = SqliteDatabase(bookmark_db_path)   # This is the database for the user's planes they bookmark.
aircraftDataDB = SqliteDatabase(aircraft_data_db_path)  # This is the database for the aircraft data, this is the data that is fetched from the API when you run the program for the first time.

class BookmarkedPlane(Model):  # This is the model for the user's planes.
    name = CharField()
    description = CharField()
    image_url = CharField()

    class Meta:
        database = bookmarkedPlaneDB

    def __str__(self):
        return f'{self.name} is {self.description}. Here\'s an image of this plane: {self.image_url}'


class AircraftData(Model):  # This is the model for the aircraft data.
    # This is the ICAO code for the aircraft. added null=True to allow for null values because some don't have an ICAO code.
    icao = CharField(null=True) # some aircraft don't have an ICAO code so we need to allow for null values, so it doesn't stop the program
    model = CharField(null=True)

    class Meta:
        database = aircraftDataDB

    def __str__(self):
        return f'{self.model} and its icao code is {self.icao_code}'


class DatabaseManager:  # This is the class that manages the database operations

    def __init__(self, api_url, access_key): # This is the constructor for the DatabaseManager class that takes in the api url and the access key.
        self.api_url = api_url
        self.access_key = access_key

    def setup_databases(self): # This function sets up the databases
        os.makedirs('database', exist_ok=True) # create the database folder if it doesn't exist already
        bookmarkedPlaneDB.connect()
        aircraftDataDB.connect()
        bookmarkedPlaneDB.create_tables([BookmarkedPlane])
        aircraftDataDB.create_tables([AircraftData])


    # this function fetches the data from the API and stores it in the database. Will break it up into smaller functions later.
    def fetch_and_store_airplane_data(self):
        try:
            response = requests.get(
                f'{self.api_url}?access_key={self.access_key}&limit=10000') # This is the api url with the access key and the limit of 10000 to get a lot of data but the limit is a lot higher than 10k
            if response.status_code == 200:
                airplane_data = response.json()['data'] 
                for airplane in airplane_data:
                    # this will not store the icao and model we get into aircraftDB
                    AircraftData.create(
                        model=airplane['production_line'],
                        icao=airplane['iata_code_long']
                    )
            else:
                print(f'Failed to retrieve data: {response.status_code}')
        except Exception as e:
            print(f'Failed to retrieve data: {e}')

    # This function shows all the bookmarked planes
    def show_bookmarked_planes(self):
        return BookmarkedPlane.select() 

    def create_plane(self, plane, description):
        # This checks to see if the plane already exists in the database.
        existing_plane = BookmarkedPlane.get_or_none(BookmarkedPlane.name == plane)
        if existing_plane is None: # if the plane doesn't exist in the database then it will create it.
            plane = BookmarkedPlane(name=plane, description=description)
            plane.save()
        else:
            print(f'Plane with name {plane} already exists.')

    def delete_plane_by_model_or_dbID(self, model_or_dbID):
        try:
            dbID = int(model_or_dbID) # turn the string number into an integer
            plane = BookmarkedPlane.get_or_none(
                (BookmarkedPlane.id == dbID) | (BookmarkedPlane.name == model_or_dbID)) # now they can delete by the name or the database unique ID
        except ValueError: # this will catch if they int and it will get plane by model name
            plane = BookmarkedPlane.get_or_none(BookmarkedPlane.name == model_or_dbID)

        if plane is not None: 
            plane.delete_instance()
            print(f'Successfully deleted plane: {model_or_dbID}.')
        else:
            print(f'No plane found with name or ID {model_or_dbID}.')

    def search_plane(self, plane_name):
        # This searches for the plane in the database
        plane = BookmarkedPlane.get_or_none(BookmarkedPlane.name == plane_name) 
        # This checks to see if the plane exists in the database
        if plane is not None: 
            return str(plane) # This returns the plane as a string
        else:
            print(f'No plane found with name {plane_name}.')
