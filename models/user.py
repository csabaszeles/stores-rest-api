import sqlite3
from db import db




#######################################################################################
# model: our internal representation of an entity (/ a helper, not a resource)
# resource: an external representation of an entity
## an API respons with resources (to our client, i.e.: web app or mobile app)
#######################################################################################

# User model
class UserModel(db.Model):
    __tablename__ = "users"

    # SQL will look at these properties of the class (names must match) to save into the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    ## Note: because id is a primary_key -> auto-incrementing, SQLAlchemy engine will automatically create an id for us when we create the object
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
