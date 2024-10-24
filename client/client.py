import socket
import ssl
import threading

SERVER_HOST = "localhost"
PORT = 10001

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_verify_locations("../cert.pem")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = context.wrap_socket(client_socket, server_hostname=SERVER_HOST)
client.connect((SERVER_HOST, PORT))

username = ""


def receive():
    global username

    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message == "SERVER SHUTDOWN":
                print("Server has shut down. Disconnecting...")
                client.close()
                break
            elif message == "Type '1' to register or '2' to login: ":
                user_option = input(message).strip()
                client.send(user_option.encode("utf-8"))
            elif message == "Enter username: ":
                username = input(message).strip()
                client.send(username.encode("utf-8"))
            elif message == "Enter password: ":
                password = input(message).strip()
                client.send(password.encode("utf-8"))
            else:
                print(message)

        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = input("").strip()
        if not message:
            continue

        client.send(f"{username}: {message}".encode("utf-8"))


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
