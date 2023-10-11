from peewee import *
import os
import requests
from dotenv import load_dotenv

load_dotenv()

db_1 = os.path.join('database', 'planes.sqlite') # This is the database for the user's planes.
db_2 = os.path.join('database', 'aircraft.sqlite') 

userPlaneDB = SqliteDatabase(db_1)
aircraftDB = SqliteDatabase(db_2)


class Plane(Model): # This is the model for the user's planes.
    name = CharField()
    description = CharField()

    class Meta:
        database = userPlaneDB

    def __str__(self):
        return f'{self.name} is {self.description}'


class UserPlane(Model): # This is the model for the aircraft data.
    icao = CharField(null=True) # This is the ICAO code for the aircraft. added null=True to allow for null values because some don't have an ICAO code.
    model = CharField(null=True)

    class Meta:
        database = aircraftDB

    def __str__(self):
        return f'{self.model} and its icao code is {self.icao_code}'


class DatabaseManager: # This is the class that manages the database operations 
    
    def __init__(self, api_url, access_key):
        self.api_url = api_url
        self.access_key = access_key
    
    def setup_databases(self):
        os.makedirs('database', exist_ok=True)
        aircraftDB.connect()
        userPlaneDB.connect()
        userPlaneDB.create_tables([Plane])
        aircraftDB.create_tables([UserPlane])

    def fetch_and_store_airplane_data(self): # this function fetches the data from the API and stores it in the database. Will break it up into smaller functions later.
        try:
            response = requests.get(f'{self.api_url}?access_key={self.access_key}&limit=10000')
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


    def show_bookmarked_planes(): # This function shows all the bookmarked planes
        return Plane.select()


    def create_plane(plane, description):
        existing_plane = Plane.get_or_none(Plane.name == plane) # This checks to see if the plane already exists in the database.
        if existing_plane is None:
            plane = Plane(name=plane, description=description)
            plane.save()
        else:
            print(f'Plane with name {plane} already exists.')


    def delete_plane(delete_plane):
        plane = Plane.get_or_none(Plane.name == delete_plane)
        if plane is not None:
            plane.delete_instance()
        else:
            print(f'No plane found with name {delete_plane}.')


    def search_plane(plane_name):
        plane = Plane.get_or_none(Plane.name == plane_name) # This searches for the plane in the database 
        if plane is not None:
            return str(plane)
        else:
            print(f'No plane found with name {plane_name}.')



    
    

