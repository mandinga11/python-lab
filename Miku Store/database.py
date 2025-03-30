from peewee import *
from decouple import config

import datetime

database = MySQLDatabase(
    config('DB_NAME'),
    user=config('USER'),
    password=config('PASSWORD'),
    port=3306,
    host=config('HOST')
)

class User(Model):
    email = TextField()
    password = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = database
        db_table = 'Users'
        
        
database.create_tables( [User] )