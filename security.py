# from werkzeug.security import safe_str_cmp    # removed in version 2.1.0 -- https://werkzeug.palletsprojects.com/en/2.1.x/changes/#version-2-1-0
import hmac

from models.user import UserModel

# username_mapping:
# "bob": {
#         "id": 1,
#         "username": 'bob',
#         "password": "asdf"
#     }
# username_mapping["bob"]

# userid_mapping:
# 1:  {
#         "id": 1,
#         "username": 'bob',
#         "password": "asdf"
# }
# userid_mapping[1]

###################################################################################

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

# payload is the content of the JWT token
def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)

