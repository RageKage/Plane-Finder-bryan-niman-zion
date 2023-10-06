from peewee import *

db = SqliteDatabase('database\planes.sqlite')

class Plane(Model):
    name = CharField()
    description = CharField()

    class Meta:
        database = db

    def __str__(self):
        return f'{self.name} is {self.description}'

db.connect()
db.create_tables([Plane])