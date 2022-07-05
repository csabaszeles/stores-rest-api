from db import db



class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")   # this is a list, because this is a many-to-one relationship
                                                           # if lazy="dynamic", then not list, but a query-builder
                                    # lazy="dynamic" tradeoff: table creation is faster, but calling json() every time (i.e.: look into the table) is slower


    def __init__(self, name):
        self.name = name

    # until we call the json() method, we don't look into the json() method
    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # line below is a query builder : cls.query. ...
        # can build queries, like: "ItemModel.query.filter_by(name=name).filer_by(id=1)" or "ItemModel.query.filter_by(name=name, id=1)"

        # this returns an ItemModel object (i.e.: SQL converts the row back to an object)
        # cls.query.filter_by(name=name).first()

        return cls.query.filter_by(name=name).first()   # SELECT * FROM items WHERE name=name LIMIT 1


    # this is good for inserting and updating too ("upsert")
    def save_to_db(self):
        # we can add multiple objects to the session (/and write them all at once )
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()