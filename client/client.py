import socket
import ssl
import sys
from PyQt6.QtWidgets import QApplication
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
            print(f"********** Server Error: {e} **********")

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.sendall(message.encode('utf-8'))

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    return message
            except:
                break

    def start_gui(self):
        app = QApplication(sys.argv)
        login_window = LoginScreen(self)
        login_window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.start_gui()
