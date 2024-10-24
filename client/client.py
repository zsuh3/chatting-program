import socket
import ssl
import threading
import tkinter as tk
from frontend.login_register import LoginScreen


class Client:
    def __init__(self, host="localhost", port=10001):
        self.host = host
        self.port = port
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_verify_locations("../cert.pem")
        self.client_socket = None
        self.client = None
        self.username = ""
        self.gui = None
        self.register_login_timeout = 1.0
        self.chat_timeout = 100.0

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client = self.context.wrap_socket(self.client_socket, server_hostname=self.host)
            self.client.settimeout(self.register_login_timeout)
            self.client.connect((self.host, self.port))
            print("********** Server Connection Successful **********")
        except Exception as e:
            print(f"********** Server Connection Error: {e} **********")

    def send_message(self, message):
        if self.client:
            try:
                self.client.send(message.encode('utf-8'))
                print(f"Sent: {message}")
            except Exception as e:
                print(f"********** Send Message Error **********")

    def receive_message(self):
        try:
            while True:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    print("********** Server closed connection **********")
                    self.client.close()
                    break

                print(f"Received: {message}")

                if message == "SERVER SHUTDOWN":
                    print("Server has shut down. Disconnecting...")
                    self.client.close()
                    break

                elif "Username already exists" in message:
                    if self.gui:
                        self.gui.display_error("Registration failed: Username already exists.")
                elif "Login successful" in message:
                    if self.gui:
                        self.gui.switch_to_chat()
                elif "Registration successful" in message:
                    if self.gui:
                        self.gui.switch_to_chat()
                elif "Invalid password" in message or "User not found" in message:
                    if self.gui:
                        self.gui.display_error(message)

                else:
                    if self.gui:
                        self.gui.display_error(message)

        except Exception as e:
            print(f"********** Receive Message Error: {e} **********")

    def process_message(self, message):
        message_split = message.split(":")
        print("PROCESS message here")

        if len(message_split) == 3:
            command = message_split[0].strip()
            username = message_split[1].strip()
            password = message_split[2].strip()

            if command == "REGISTER":
                print(f"Registering with username: {username}, password: {password}")
                self.send_message(f"REGISTER:{username}:{password}")
            elif command == "LOGIN":
                print(f"Logging in with username: {username}, password: {password}")
                self.send_message(f"LOGIN:{username}:{password}")
        else:
            print(f"********** Invalid message format: {message}")

    def update_timeout(self, timeout):
        if self.client:
            try:
                self.client.settimeout(timeout)
                print(f"********** Timeout updated to {timeout} seconds **********")
            except Exception as e:
                print(f"********** Error updating timeout: {e} **********")

    def start_receive_thread(self):
        receive_thread = threading.Thread(target=self.receive_message, daemon=True)
        receive_thread.start()

    def start_gui(self):
        root = tk.Tk()
        self.gui = LoginScreen(root, self)
        self.start_receive_thread()
        root.mainloop()


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.start_gui()
