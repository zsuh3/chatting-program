from .chat import ChatScreen
import tkinter as tk
# from tkmacosx import Button

LABEL_TEXT_FONT = ("Arial", 16, "bold")
INPUT_TEXT_FONT = ("Arial", 16)
BUTTON_TEXT_FONT = ("Arial", 18)
ERROR_TEXT_FONT = ("Arial", 12, "bold")


class LoginScreen:
    def __init__(self, root, client_app):
        self.root = root
        self.client_app = client_app
        self.root.title("Register / Login")
        self.root.geometry("736x414")
        self.root.config(bg="#EDDFE0")

        spacer = tk.Label(root, text="", height=2, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # username
        self.username_label = tk.Label(root, text="Enter Username:", font=LABEL_TEXT_FONT, bg="#EDDFE0", fg="#705C53")
        self.username_label.pack(pady=5)
        self.username_input = tk.Entry(root, font=INPUT_TEXT_FONT, bg="#EDDFE0", fg="#705C53", relief="flat")
        self.username_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.username_input.insert(0, "username")
        self.username_input.bind("<FocusIn>", self.clear_text)
        self.username_input.pack()

        spacer = tk.Label(root, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # password
        self.password_label = tk.Label(root, text="Enter Password:", font=LABEL_TEXT_FONT, bg="#EDDFE0", fg="#705C53")
        self.password_label.pack(pady=5)
        self.password_input = tk.Entry(root, font=INPUT_TEXT_FONT, bg="#EDDFE0", fg="#705C53", relief="flat")
        self.password_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.password_input.insert(0, "password")
        self.password_input.bind("<FocusIn>", self.clear_text)
        self.password_input.pack()

        spacer = tk.Label(root, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # register
        self.register_button = tk.Button(root, text="Sign Up", command=self.register, font=BUTTON_TEXT_FONT,
                                         bg="#705C53", fg="#F5F5F7", activebackground="#705C53",
                                         activeforeground="#F5F5F7", borderwidth=0, highlightthickness=2,
                                         highlightbackground="#705C53", relief="flat")
        self.register_button.pack()

        spacer = tk.Label(root, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # switch to login
        self.login_button = tk.Button(root, text="Already have an account? Sign In", command=self.switch_to_login,
                                      font=BUTTON_TEXT_FONT, bg="#705C53", fg="#F5F5F7", activebackground="#705C53",
                                      activeforeground="#F5F5F7", borderwidth=0, highlightthickness=0,
                                      highlightcolor="#705C53", relief="flat")
        self.login_button.pack()

        spacer = tk.Label(root, text="", height=1, bg="#EDDFE0", fg="#705C53")
        spacer.pack()

        # invalid input
        self.error_label = tk.Label(root, text="", bg="#EDDFE0", fg="#C96868", font=ERROR_TEXT_FONT)
        self.error_label.pack()

    def clear_text(self, event):
        if event.widget == self.username_input and self.username_input.get() == "username":
            self.username_input.delete(0, tk.END)
            self.username_input.config(show="")
        elif event.widget == self.password_input and self.password_input.get() == "password":
            self.password_input.delete(0, tk.END)
            self.password_input.config(show="*")

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
