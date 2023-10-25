from peewee import *
import os
import requests


# path of the user db for bookmarked planes
bookmark_db_path = os.path.join('database', 'bookmarked_planes.sqlite')
aircraft_data_db_path = os.path.join(
    'database', 'aircraft_data.sqlite')  # path aircraft data db


bookmarkedPlaneDB = SqliteDatabase(bookmark_db_path)
aircraftDataDB = SqliteDatabase(aircraft_data_db_path)


class BookmarkedPlane(Model):
    """This class represents a bookmarked plane."""
    name = CharField()
    description = CharField()
    image_url = CharField()

    class Meta:
        database = bookmarkedPlaneDB

    def __str__(self):
        return f'Model name: ({self.name}) is {self.description}. Here\'s an image of this plane: {self.image_url}'


class AircraftData(Model):
    """This class represents an aircraft."""
    icao = CharField(null=True)
    model = CharField(null=True)

    class Meta:
        database = aircraftDataDB

    def __str__(self):
        return f'{self.model} and its icao code is {self.icao}'


class DatabaseManager:
    """This class represents the database manager. Which is responsible for managing the database."""

    def __init__(self, api_url, access_key):
        """This initializes the database manager."""
        self.api_url = api_url
        self.access_key = access_key

    def setup_databases(self):
        """this sets the database by creating the database folder and the database files."""
        os.makedirs('database', exist_ok=True)
        bookmarkedPlaneDB.connect()
        aircraftDataDB.connect()
        bookmarkedPlaneDB.create_tables([BookmarkedPlane])
        aircraftDataDB.create_tables([AircraftData])

    def fetch_airplane_data(self):
        """This function fetches the data from the api and stores it into the database."""
        try:
            response = requests.get(
                f'{self.api_url}?access_key={self.access_key}&limit=10000')
            if response.status_code == 200:
                airplane_data = response.json()['data']
                self.store_airplane_data(airplane_data)

            else:
                print(f'Failed to retrieve data: {response.status_code}')
        except Exception as e:
            print(f'Failed to retrieve data: {e}')

    def store_airplane_data(self, airplane_data):
        """This function stores the data into the database."""
        for airplane in airplane_data:
            AircraftData.create(
                model=airplane['production_line'], icao=airplane['iata_code_long'])

    def show_bookmarked_planes(self):
        """This function shows all the bookmarked planes in the database."""
        return BookmarkedPlane.select()

    def create_plane(self, plane, description):
        """This function creates a plane and adds it to the database."""
        existing_plane = BookmarkedPlane.get_or_none(
            BookmarkedPlane.name == plane)
        if existing_plane is None:
            plane = BookmarkedPlane(name=plane, description=description)
            plane.save()
        else:
            print(f'Plane with name {plane} already exists.')

    def delete_plane_by_model(self, model_name):
        """Deletes a plane by model name."""
        try:
            plane = BookmarkedPlane.get_or_none(BookmarkedPlane.name == model_name)
            if plane is not None:
                plane.delete_instance()
                print(f'Successfully deleted plane: {model_name}.')
            else:
                print(f'No plane found with model name {model_name}.')
        except Exception as e:
            print(f'Failed to delete plane: {e}')

    def search_plane(self, plane_name):
        """This function searches for a plane in the database and returns the plane."""
        plane = BookmarkedPlane.get_or_none(BookmarkedPlane.name == plane_name)
        if plane is not None:
            return str(plane)
        else:
            print(f'No plane found with name {plane_name}.')

    def search_aircraft_by_model(self, model):
        """This function searches for a plane in the database and returns a list of planes. (planes might have the same model name but different icao codes)"""
        aircrafts = AircraftData.select().where(AircraftData.model.contains(model))
        return list(aircrafts)

    def search_aircraft_by_icao(self, icao):
        """this function searches for a plane in the database by icao code and returns the plane object."""
        aircraft = AircraftData.get_or_none(AircraftData.icao == icao)
        if aircraft:
            return aircraft
        else:
            print(f'No plane found with icao {icao}.')
            return None
