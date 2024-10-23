import json
import os


def load_users():
    if not os.path.exists("../users.json"):
        with open("../users.json", "w") as file:
            json.dump({}, file)

    with open("../users.json", "r") as read_users:
        return json.load(read_users)


def save_user(user):
    with open("../users.json", "w") as write_user:
        json.dump(user, write_user)

