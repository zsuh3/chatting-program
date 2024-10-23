import json


def load_users():
    with open("users.json", "r") as read_users:
        return json.load(read_users)


def save_user(user):
    with open("users.json", "w") as write_user:
        json.dump(user, write_user)

