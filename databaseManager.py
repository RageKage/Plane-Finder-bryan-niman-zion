from peewee import *
import os
import requests

# This is the database for the user's planes.
db_1 = os.path.join('database', 'planes.sqlite')
db_2 = os.path.join('database', 'aircraft.sqlite')

userPlaneDB = SqliteDatabase(db_1)
aircraftDB = SqliteDatabase(db_2)


class Plane(Model):  # This is the model for the user's planes.
    name = CharField()
    description = CharField()

    class Meta:
        database = userPlaneDB

    def __str__(self):
        return f'{self.name} is {self.description}'


class UserPlane(Model):  # This is the model for the aircraft data.
    # This is the ICAO code for the aircraft. added null=True to allow for null values because some don't have an ICAO code.
    icao = CharField(null=True)
    model = CharField(null=True)

    class Meta:
        database = aircraftDB

    def __str__(self):
        return f'{self.model} and its icao code is {self.icao_code}'


class DatabaseManager:  # This is the class that manages the database operations

    def __init__(self, api_url, access_key):
        self.api_url = api_url
        self.access_key = access_key

    def setup_databases(self):
        os.makedirs('database', exist_ok=True)
        aircraftDB.connect()
        userPlaneDB.connect()
        userPlaneDB.create_tables([Plane])
        aircraftDB.create_tables([UserPlane])

    # this function fetches the data from the API and stores it in the database. Will break it up into smaller functions later.
    def fetch_and_store_airplane_data(self):
        try:
            response = requests.get(
                f'{self.api_url}?access_key={self.access_key}&limit=10000')
            if response.status_code == 200:
                airplane_data = response.json()['data']
                for airplane in airplane_data:
                    UserPlane.create(
                        model=airplane['production_line'],
                        icao=airplane['iata_code_long']
                    )
            else:
                print(f'Failed to retrieve data: {response.status_code}')
        except Exception as e:
            print(f'Failed to retrieve data: {e}')

    # This function shows all the bookmarked planes
    def show_bookmarked_planes(self):
        return Plane.select()

    def create_plane(self, plane, description):
        # This checks to see if the plane already exists in the database.
        existing_plane = Plane.get_or_none(Plane.name == plane)
        if existing_plane is None:
            plane = Plane(name=plane, description=description)
            plane.save()
        else:
            print(f'Plane with name {plane} already exists.')

    def delete_plane_by_model_or_dbID(self, model_or_dbID):
        try:
            dbID = int(model_or_dbID) # turn the string number into an integer
            plane = Plane.get_or_none(
                (Plane.id == dbID) | (Plane.name == model_or_dbID)) # now they can delete by the name or the database unique ID
        except ValueError: # this will catch if they int and it will get plane by model name
            plane = Plane.get_or_none(Plane.name == model_or_dbID)

        if plane is not None:
            plane.delete_instance()
            print(f'Successfully deleted plane: {model_or_dbID}.')
        else:
            print(f'No plane found with name or ID {model_or_dbID}.')

    def search_plane(self, plane_name):
        # This searches for the plane in the database
        plane = Plane.get_or_none(Plane.name == plane_name)
        if plane is not None:
            return str(plane)
        else:
            print(f'No plane found with name {plane_name}.')
