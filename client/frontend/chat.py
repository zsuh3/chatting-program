import threading
import tkinter as tk
from tkinter import scrolledtext


class ChatScreen:
    def __init__(self, root, client_app):
        self.root = root
        self.client_app = client_app
        self.root.title("Chat Room")
        self.root.geometry("736x414")
        self.root.config(bg="#EDDFE0")

        # chat area
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 18), bg="#F5F5F7",
                                                   fg="#705C53", highlightthickness=2, highlightbackground="#B7B7B7",
                                                   state="disabled", height=10)
        self.chat_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # message area
        self.message_input = tk.Entry(self.root, font=("Arial", 16), bg="#EDDFE0", fg="#705C53", relief="flat")
        self.message_input.config(highlightbackground="#B7B7B7", highlightcolor="#B7B7B7")
        self.message_input.pack(padx=20, pady=10, fill=tk.X)
        self.message_input.bind("<Return>", self.send_message)

        # send
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, font=("Arial", 18),
                                     bg="#705C53", fg="#F5F5F7", activebackground="#705C53", activeforeground="#F5F5F7",
                                     borderwidth=0, highlightthickness=2, highlightbackground="#705C53", relief="flat")
        self.send_button.pack(padx=20, pady=20, fill=tk.X)

        self.listen_for_messages()

    def send_message(self, event=None):
        message = self.message_input.get()
        if message:
            self.client_app.send_message(message)
            self.append_message(f"You: {message}")
            self.message_input.delete(0, tk.END)

    def append_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def listen_for_messages(self):
        def listen():
            while True:
                message = self.client_app.receive_message()
                if message:
                    self.append_message(message)

        threading.Thread(target=listen, daemon=True).start()
