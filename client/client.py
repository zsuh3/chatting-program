import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 10001))

username = ""


def receive():
    global username

    while True:
        try:
            message = client.recv(1024).decode("ascii")

            if message == "SERVER SHUTDOWN":
                print("Server has shut down. Disconnecting...")
                client.close()
                break
            elif message == "Type 1 to register or 2 to login: ":
                user_option = input(message)
                client.send(user_option.encode("ascii"))
            elif message == "Enter username: ":
                username = input(message)
                client.send(username.encode("ascii"))
            elif message == "Enter password: ":
                password = input(message)
                client.send(password.encode("ascii"))
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

        client.send(f"{username}: {message}".encode("ascii"))


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
