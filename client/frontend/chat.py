from PyQt6.QtWidgets import QWidget


class ChatScreen(QWidget):
    def __init__(self, client_app):
        super().__init__()
        self.client_app = client_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat")
        pass
