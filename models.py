from peewee import *

db = SqliteDatabase("project.db")

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()



db.connect()
db.create_tables([User,])
#runs only once till there are no updates in list
