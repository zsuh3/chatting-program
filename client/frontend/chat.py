import tkinter as tk


class ChatScreen:
    def __init__(self, root, client_app):
        self.root = root
        self.client_app = client_app
        self.root.title("Chat")
        self.root.geometry("736x414")
        self.root.config(bg="#EDDFE0")

        pass
