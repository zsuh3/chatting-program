import socket
import ssl
import tkinter as tk
from frontend.login_register import LoginScreen


class Client:
    def __init__(self, host="localhost", port=10001):
        self.host = host
        self.port = port
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_verify_locations("../cert.pem")
        self.client_socket = None
        self.username = ""

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client = self.context.wrap_socket(self.client_socket, server_hostname=self.host)
            self.client.connect((self.host, self.port))
            print("********** Server Connection Successful **********")
        except Exception as e:
            print(f"********** Server Connection Error: {e} **********")

    def send_message(self, message):
        if self.client_socket:
            try:
                self.client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"********** Send Message Error  **********")

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    return message
            except Exception as e:
                print(f"********** Receive Message Error **********")
                return None

    def start_gui(self):
        root = tk.Tk()
        login_screen = LoginScreen(root, self)
        root.mainloop()


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.start_gui()
