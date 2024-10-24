import socket
import ssl
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkmacosx import Button

PORT = 10001
SERVER = "localhost"
FORMAT = "utf-8"

LABEL_TEXT_FONT = ("Arial", 16, "bold")
INPUT_TEXT_FONT = ("Arial", 16)
BUTTON_TEXT_FONT = ("Arial", 18)
ERROR_TEXT_FONT = ("Arial", 14, "bold")


class Client(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chat Client")
        self.geometry("736x414")

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.client_socket = None
        self.connect()

        self.register_login = tk.Frame(self, bg="#EDDFE0")
        self.chat = tk.Frame(self, bg="#EDDFE0")
        self.initialise_register_login()
        self.initialise_chat()
        self.register_login.pack(expand=True, fill="both")

        self.username = ""

    def connect(self):
        """ Connect client to server"""

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket = self.context.wrap_socket(self.client_socket, server_hostname=SERVER)
            self.client_socket.connect((SERVER, PORT))
            print("Connected to the server.")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")
            messagebox.showerror("Connection Error", "Failed to connect to the server.")
            self.destroy()

    def initialise_register_login(self):
        spacer = tk.Label(self.register_login, text="", height=3, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # username area
        self.username_label = tk.Label(self.register_login, text="Enter Username:", font=LABEL_TEXT_FONT, bg="#EDDFE0",
                                       fg="#705C53")
        self.username_label.pack(pady=5)
        self.username_input = tk.Entry(self.register_login, font=INPUT_TEXT_FONT, bg="#EDDFE0", fg="#705C53",
                                       relief="flat")
        self.username_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.username_input.insert(0, "username")
        self.username_input.bind("<FocusIn>", self.clear_text)
        self.username_input.pack()

        spacer = tk.Label(self.register_login, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # password area
        self.password_label = tk.Label(self.register_login, text="Enter Password:", font=LABEL_TEXT_FONT, bg="#EDDFE0",
                                       fg="#705C53")
        self.password_label.pack(pady=5)
        self.password_input = tk.Entry(self.register_login, font=INPUT_TEXT_FONT, bg="#EDDFE0", fg="#705C53",
                                       relief="flat")
        self.password_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.password_input.insert(0, "password")
        self.password_input.bind("<FocusIn>", self.clear_text)
        self.password_input.pack()

        spacer = tk.Label(self.register_login, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # sign up button
        self.register_button = Button(self.register_login, text="Sign Up", command=self.user_register,
                                      font=BUTTON_TEXT_FONT, bg="#705C53", fg="#F5F5F7", activebackground="#705C53",
                                      activeforeground="#F5F5F7", borderwidth=0, highlightthickness=2,
                                      highlightbackground="#705C53", relief="flat")
        self.register_button.pack()

        spacer = tk.Label(self.register_login, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # sign in button
        self.login_button = Button(self.register_login, text="Sign In", command=self.user_login,
                                   font=BUTTON_TEXT_FONT, bg="#705C53", fg="#F5F5F7", activebackground="#705C53",
                                   activeforeground="#F5F5F7", borderwidth=0, highlightthickness=2,
                                   highlightbackground="#705C53", relief="flat")
        self.login_button.pack()

    def initialise_chat(self):
        self.chat_area = scrolledtext.ScrolledText(self.chat, state="disabled", wrap="word", bg="#F5F5F7", fg="#705C53",
                                                   highlightthickness=2, highlightbackground="#B7B7B7",
                                                   font=("Arial", 18), height=10)
        self.chat_area.pack(expand=True, fill="both", padx=20, pady=5)

        self.message_input = tk.Entry(self.chat, font=("Arial", 16), bg="#EDDFE0", fg="#705C53", relief="flat")
        self.message_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.message_input.pack(fill="x", padx=20, pady=10)
        self.message_input.bind("<Return>", lambda event: self.send_chat_message())

        self.send_button = tk.Button(self.chat, text="Send", command=self.send_chat_message, font=("Arial", 18),
                                     bg="#705C53", fg="#F5F5F7", activebackground="#705C53", activeforeground="#F5F5F7",
                                     borderwidth=0, highlightthickness=2, highlightbackground="#705C53", relief="flat")
        self.send_button.pack(fill="x", padx=20, pady=20)

    def clear_text(self, event):
        if event.widget == self.username_input and self.username_input.get() == "username":
            self.username_input.delete(0, tk.END)
            self.username_input.config(show="")
        elif event.widget == self.password_input and self.password_input.get() == "password":
            self.password_input.delete(0, tk.END)
            self.password_input.config(show="*")

    def user_register(self):
        """ Handle registration process """

        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        if username and password:
            self.username = username
            self.send_message(f"REGISTER:{username}:{password}")
            self.receive_response()

    def user_login(self):
        """ Handle login process """

        username = self.username_input.get().strip()
        password = self.password_input.get().strip()
        if username and password:
            self.username = username
            self.send_message(f"LOGIN:{username}:{password}")
            self.receive_response()

    def switch_to_chat(self):
        self.register_login.pack_forget()
        self.chat.pack(expand=True, fill="both")
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, message):
        """ Send message to server """

        try:
            if self.client_socket:
                self.client_socket.send(message.encode(FORMAT))
                print(f"Sent: {message}")
            else:
                print("Error: Client socket is not connected.")
        except Exception as e:
            print(f"Error sending message: {e}")

    def send_chat_message(self):
        """ Send chat message from message input """

        message = self.message_input.get().strip()
        if message:
            self.send_message(f"{self.username}: {message}")
            self.append_message(f"You: {message}")
            self.message_input.delete(0, tk.END)

    def receive_response(self):
        try:
            response = self.client_socket.recv(1024).decode(FORMAT)
            print(f"Received: {response}")
            if "successful" in response.lower():
                self.switch_to_chat()
            else:
                messagebox.showerror("Error", response)
        except Exception as e:
            print(f"Error receiving response: {e}")

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode(FORMAT)
                if not message:
                    break
                self.display_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def append_message(self, message):
        self.chat_area.config(state="normal")
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

    def display_message(self, message):
        self.after(0, self.append_message, message)


if __name__ == "__main__":
    client = Client()
    client.mainloop()
