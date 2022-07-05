import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

db_file = "data.db"


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="username field cannot be left blank"
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="password field cannot be left blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists."}, 400

        # user = UserModel(data["username"], data["password"])
        # same as above
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201


    if False:
        def get(self):
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            query = "SELECT * FROM users"

            registered_users = cursor.execute(query).fetchall()

            for user in registered_users:
                print(user)

            return {"registered users": registered_users}