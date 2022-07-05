from db import db



class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))  # items are linked to stores;
                                                                  # stores cannot be deleted before all items related to a store are deleted
    store = db.relationship("StoreModel")   # this is the store, hat matches the store_id      ### no need for join()s in SQLAlchemy


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # returns a JSON representation of the model
    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        # line below is a query builder : cls.query. ...
        # can build queries, like: "ItemModel.query.filter_by(name=name).filer_by(id=1)" or "ItemModel.query.filter_by(name=name, id=1)"

        # this returns an ItemModel object (i.e.: SQL converts the row back to an object)
        cls.query.filter_by(name=name).first()

        return cls.query.filter_by(name=name).first()   # SELECT * FROM items WHERE name=name LIMIT 1


    # this is good for inserting and updating too ("upsert")
    def save_to_db(self):
        # we can add multiple objects to the session (/and write them all at once )
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()