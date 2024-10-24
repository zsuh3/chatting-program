from .chat import ChatScreen
import tkinter as tk

TEXT_FONT = ("Arial", 16)
ERROR_TEXT_FONT = ("Arial", 12)


class LoginScreen:
    def __init__(self, root, client_app):
        self.root = root
        self.client_app = client_app
        self.root.title("Register / Login")
        self.root.geometry("736x414")
        self.root.config(bg="#EDDFE0")

        # username
        self.username_label = tk.Label(root, text="Enter Username:", font=TEXT_FONT)
        self.username_label.pack(pady=5)
        self.username_input = tk.Entry(root, font=TEXT_FONT)
        self.username_input.pack(pady=5)

        # password
        self.password_label = tk.Label(root, text="Enter Password:", font=TEXT_FONT)
        self.password_label.pack(pady=5)
        self.password_input = tk.Entry(root, font=TEXT_FONT, show="*")
        self.password_input.pack(pady=5)

        # register
        self.register_button = tk.Button(root, text="Sign Up", command=self.register, font=TEXT_FONT)
        self.register_button.pack(pady=10)

        # switch to login
        self.login_button = tk.Button(root, text="Already have an account? Sign In", command=self.switch_to_login,
                                      font=TEXT_FONT)
        self.login_button.pack(pady=10)

        # invalid input
        self.error_label = tk.Label(root, text="", fg="red", font=ERROR_TEXT_FONT)
        self.error_label.pack(pady=5)

    def switch_to_login(self):
        self.register_button.config(text="Sign In", command=self.login)
        self.login_button.config(text="Don't have an account? Sign Up", command=self.switch_to_register)

    def switch_to_register(self):
        self.register_button.config(text="Sign Up", command=self.register)
        self.login_button.config(text="Already have an account? Sign In", command=self.switch_to_login)

    def switch_to_chat(self):
        self.root.withdraw()
        chat_window = tk.Toplevel(self.root)
        ChatScreen(chat_window, self.client_app)

    def register(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            self.client_app.send_message(f"REGISTER:{username}:{password}")
            response = self.client_app.receive_message()

            if "successful" in response:
                self.switch_to_chat()
            else:
                self.error_label.config(text="Registration failed. Try again.")
        else:
            self.error_label.config(text="Username and password cannot be empty.")

    def login(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            self.client_app.send_message(f"LOGIN:{username}:{password}")
            response = self.client_app.receive_message()

            if "successful" in response:
                self.switch_to_chat()
            else:
                self.error_label.config(text="Login failed. Try again.")
        else:
            self.error_label.config(text="Username or Password cannot be empty.")
