from peewee import *

# Uses the database called planes.sqlite in the database folder, or creates one if it can't be found.
db = SqliteDatabase('database\planes.sqlite')


class Plane(Model):
    name = CharField()
    description = CharField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.name} is {self.description}'


# Returns all bookmarked planes using peewee to access the database
def get_planes():
    return Plane.select()

db.connect()
db.create_tables([Plane])