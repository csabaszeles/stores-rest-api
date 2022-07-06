# project has example requests in Postman under /Section6
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri or "sqlite:///data.db"
                                      #"sqlite:///data.db"  # this tells that our SQLAlchemy database will live in the root of our project (default is "in-memory" database)
                                      # it works not only with sqlite, but SQLAlchemy, PostgreSQL, MySQL, SQLite,,,, just we have to change this line of code
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False   # this turns off the Flask-SQLAlchemy modification tracker,
                                                       # but the main SQLAlchemy mod. track. is still working (which is a bit better)
app.secret_key = 'jose'  # this should be really a secret key!, you shouldn't publish this code
api = Api(app)

# this method is run before the first request to this app
@app.before_first_request
def create_tables():
    db.create_all()    # this creates the "sqlite:///data.db" tables, unless they exist already
                       # note: this creates tables that it sees (so those that get imported) - Worst case, just import the model directly


jwt = JWT(app, authenticate, identity_function)

db.init_app(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(port=5000, debug=True)