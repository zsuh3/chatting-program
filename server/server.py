import socket
import threading
import ssl
from user import load_users, save_user

PORT = 10001
HOST = "localhost"
FORMAT = "utf-8"

SHIFT_N = 5

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile="../cert.pem", keyfile="../cert.pem")
context.load_verify_locations("../cert.pem")
context.set_ciphers("AES128-SHA")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = context.wrap_socket(server, server_side=True)
server.bind((HOST, PORT))
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
                    encrypted_password = encrypt_password(password)
                    users[username] = encrypted_password
                    save_user(users)
                    client_socket.send("Registration successful.".encode(FORMAT))
                    break
            elif "LOGIN" in msg:
                _, username, password = msg.split(":")
                if username in users and users[username] == encrypt_password(password):
                    client_socket.send("Login successful.".encode(FORMAT))
                    break
                else:
                    client_socket.send("Invalid username and password.".encode(FORMAT))

        clients.add(client_socket)
        broadcast(f"{username} has joined the chat.", client_socket)

        while True:
            msg = client_socket.recv(1024).decode(FORMAT)
            if not msg:
                break
            broadcast(msg, client_socket)

    finally:
        clients.remove(client_socket)
        client_socket.close()


def encrypt_password(password, shift=SHIFT_N):
    encrypted_password = ""
    for char in password:
        if char.isalpha():
            if char.isupper():
                encrypted_password += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                encrypted_password += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            encrypted_password += char
    return encrypted_password


def broadcast(msg, sender=None):
    """ Broadcast to all clients except sender """

    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode(FORMAT))
            except:
                client.close()
                clients.remove(client)


def start_server():
    print(f"*** Server is listening ***")
    print(f"*** Connected with ('{HOST}', {PORT}) ***")

    while True:
        client_socket, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
