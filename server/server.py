import socket
import threading
import user

host = "127.0.0.1"
port = 10001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []


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

        client.send("USER".encode("ascii"))
        username = client.recv(1024).decode("ascii")
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
    users = user.load_users()

    client.send("Enter username: ".encode("ascii"))
    username = client.recv(1024).decode("ascii")

    if username in users:
        client.send("Username already exists. Try a different username.")
    else:
        client.send("Enter password: ".encode("ascii"))
        password = client.recv(1024).decode("ascii")

        users[username] = password
        user.save_user(users)
        client.send(f"{username} successfully registered!")


def login_user():
    pass


if __name__ == "__main__":
    print("Server is listening...")

    command_thread = threading.Thread(target=server_commands)
    command_thread.start()

    receive()
