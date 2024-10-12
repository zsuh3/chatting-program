import socket
import threading

username = input("Enter your username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 10001))


def receive():
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "USER":
                client.send(username.encode("ascii"))
            elif message == "SERVER SHUTDOWN":
                print("Server has shut down. Disconnecting...")
                client.close()
                break
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        message = input("")
        if message.lower() == "/leave":
            client.close()
            break
        else:
            client.send(f"{username}: {message}".encode("ascii"))


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
