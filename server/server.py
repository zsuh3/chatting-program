import socket
import ssl
import threading
from user import load_users, save_user

SERVER_HOST = "localhost"
PORT = 10001
BACKLOG = 5

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile="../cert.pem", keyfile="../cert.pem")
context.load_verify_locations("../cert.pem")
context.set_ciphers("AES128-SHA")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((SERVER_HOST, PORT))
server.listen(BACKLOG)

server = context.wrap_socket(server, server_side=True)

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
            broadcast(f"{username} left the chat!".encode("utf-8"))
            usernames.remove(username)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        while True:
            # debugging print statements
            print("***** Waiting for message *****")
            message = client.recv(1024).decode("utf-8")
            print(message)
            print("***** Received message *****")

            if "REGISTER" in message:
                # register
                register_successful, username = process_register(client, message)
                if register_successful:
                    break
            elif "LOGIN" in message:
                # login
                login_successful, username = process_login(client, message)
                if login_successful:
                    break
            else:
                client.send("Invalid option. Try again.\n".encode("utf-8"))

        # successful registration or login
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client: {username}")
        client.send("Connected to the server!\n".encode("utf-8"))
        broadcast(f"{username} has joined the chat!".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def process_register(client, message):
    try:
        _, username, password = message.split(":")
    except ValueError:
        client.send("Invalid registration format. Use REGISTER:username:password.\n".encode("utf-8"))
        return False, None

    if username in users:
        client.send("Username already exists. Try a different username.\n".encode("utf-8"))
        return False, None
    else:
        users[username] = password
        save_user(users)
        client.send("Registration successful!\n".encode("utf-8"))
        return True, username


def process_login(client, message):
    try:
        _, username, password = message.split(":")
    except ValueError:
        client.send("Invalid login format. Use LOGIN:username:password.\n".encode("utf-8"))
        return False, None

    if username in users:
        if users[username] == password:
            client.send("Login successful!\n".encode("utf-8"))
            return True, username
        else:
            client.send("Invalid password. Try again.\n".encode("utf-8"))
            return False, None
    else:
        client.send(f"User {username} not found.\n".encode("utf-8"))
        return False, None


def server_commands():
    while True:
        command = input("")
        if command.lower() == "/quit":
            broadcast("SERVER SHUTDOWN".encode("utf-8"))
            server.close()
            break


def register_user(client):
    client.send("Enter username: ".encode("utf-8"))
    username = client.recv(1024).decode("utf-8")

    if username in users:
        client.send("Username already exists. Try a different username.".encode("utf-8"))
        return False, None
    else:
        client.send("Enter password: ".encode("utf-8"))
        password = client.recv(1024).decode("utf-8")

        users[username] = password
        save_user(users)
        client.send("Registration successful!".encode("utf-8"))
        return True, username


def login_user(client):
    client.send("Enter username: ".encode("utf-8"))
    username = client.recv(1024).decode("utf-8")

    if username in users:
        client.send("Enter password: ".encode("utf-8"))
        password = client.recv(1024).decode("utf-8")

        if users[username] == password:
            client.send("Login successful!".encode("utf-8"))
            return True, username
        else:
            client.send("Invalid password. Try again.".encode("utf-8"))
            return False, None
    else:
        client.send(f"{username} not found!".encode("utf-8"))
        return False, None


if __name__ == "__main__":
    print("Server is listening...")

    command_thread = threading.Thread(target=server_commands)
    command_thread.start()

    receive()
