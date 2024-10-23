import json


def load_users():
    with open("users.json", "r") as read_users:
        return json.load(read_users)


def save_user(user):
    pass

