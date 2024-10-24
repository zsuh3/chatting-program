import socket
import threading
import ssl
from user import load_users, save_user

PORT = 10001
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile="../cert.pem", keyfile="../cert.pem")
context.load_verify_locations("../cert.pem")
context.set_ciphers("AES128-SHA")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = context.wrap_socket(server, server_side=True)
server.bind(ADDR)
server.listen()

clients = set()
users = load_users()


def handle_client(client_socket):
    try:
        username = None
        while True:
            msg = client_socket.recv(1024).decode(FORMAT)

            if "REGISTER" in msg:
                _, username, password = msg.split(":")
                if username in users:
                    client_socket.send("Username already exists.".encode(FORMAT))
                else:
                    users[username] = password
                    save_user(users)
                    client_socket.send("Registration successful.".encode(FORMAT))
                    break
            elif "LOGIN" in msg:
                _, username, password = msg.split(":")
                if username in users and users[username] == password:
                    client_socket.send("Login successful.".encode(FORMAT))
                    break
                else:
                    client_socket.send("Invalid credentials.".encode(FORMAT))

        clients.add(client_socket)
        broadcast(f"{username} has joined the chat.", client_socket)

        while True:
            msg = client_socket.recv(1024).decode(FORMAT)
            if not msg:
                break
            broadcast(f"{username}: {msg}", client_socket)

    finally:
        clients.remove(client_socket)
        client_socket.close()


def broadcast(msg, sender=None):
    """Send the message to all clients."""
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode(FORMAT))
            except:
                client.close()
                clients.remove(client)


def start_server():
    print(f"[LISTENING] Server is listening on {ADDR}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
