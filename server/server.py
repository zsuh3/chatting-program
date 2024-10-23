import socket
import threading
from user import load_users, save_user

host = "127.0.0.1"
port = 10001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []

users = load_users()


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f"{username} left the chat!".encode("ascii"))
            usernames.remove(username)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        while True:
            # debugging print statements
            client.send("Type 1 to register or 2 to login: ".encode("ascii"))
            print("***** Waiting for option *****")
            option = client.recv(1024).decode("ascii")
            print("***** Received option *****")

            if option == "1":
                # register
                register_successful, username = register_user(client)
                if register_successful:
                    break
            elif option == "2":
                # login
                login_successful, username = login_user(client)
                if login_successful:
                    break
            else:
                client.send("Invalid option. Try again.\n".encode("ascii"))

        # successful registration or login
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client: {username}")
        client.send("Connected to the server!\n".encode("ascii"))
        broadcast(f"{username} has joined the chat!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def server_commands():
    while True:
        command = input("")
        if command.lower() == "/quit":
            broadcast("SERVER SHUTDOWN".encode("ascii"))
            server.close()
            break


def register_user(client):
    client.send("Enter username: ".encode("ascii"))
    username = client.recv(1024).decode("ascii")

    if username in users:
        client.send("Username already exists. Try a different username.".encode("ascii"))
        return False, None
    else:
        client.send("Enter password: ".encode("ascii"))
        password = client.recv(1024).decode("ascii")

        users[username] = password
        save_user(users)
        client.send("Registration successful!".encode("ascii"))
        return True, username


def login_user(client):
    client.send("Enter username: ".encode("ascii"))
    username = client.recv(1024).decode("ascii")

    if username in users:
        client.send("Enter password: ".encode("ascii"))
        password = client.recv(1024).decode("ascii")

        if users[username] == password:
            client.send("Login successful!".encode("ascii"))
            return True, username
        else:
            client.send("Invalid password. Try again.".encode("ascii"))
            return False, None
    else:
        client.send(f"{username} not found!".encode("ascii"))
        return False, None


if __name__ == "__main__":
    print("Server is listening...")

    command_thread = threading.Thread(target=server_commands)
    command_thread.start()

    receive()
