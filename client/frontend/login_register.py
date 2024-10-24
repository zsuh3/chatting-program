from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QSpacerItem, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .chat import ChatScreen


class LoginScreen(QWidget):
    def __init__(self, client_app):
        super().__init__()
        self.client_app = client_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register / Login")
        self.setGeometry(0, 0, 736, 414)
        self.setStyleSheet("background-color: #EDDFE0; color: #705C53;")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form_layout = QFormLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # username
        self.username_label = QLabel("Enter Username: ")
        self.username_label.setStyleSheet("font-size: 16px;")
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("username")
        self.username_input.setStyleSheet("font-size: 16px; padding: 6px;")
        self.username_input.setFixedWidth(175)
        form_layout.addRow(self.username_label, self.username_input)

        # password
        self.password_label = QLabel("Enter Password: ")
        self.password_label.setStyleSheet("font-size: 16px;")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("password")
        self.password_input.setStyleSheet("font-size: 16px; padding: 6px;")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(175)
        form_layout.addRow(self.password_label, self.password_input)

        form_layout.addItem(QSpacerItem(1, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        # register
        self.register_button = QPushButton("Sign Up", self)
        self.register_button.clicked.connect(self.register)
        self.register_button.setStyleSheet("background-color: #705C53; color: #F5F5F7; padding: 10px; font-size: 16px;")
        self.register_button.setFixedWidth(300)
        form_layout.addRow(self.register_button)

        form_layout.addItem(QSpacerItem(1, 3, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        # switch to login
        self.login_button = QLineEdit(self)
        self.login_button = QPushButton("Already have an account? Sign Up", self)
        self.login_button.clicked.connect(self.switch_to_login)
        self.login_button.setStyleSheet("background-color: #705C53; color: #F5F5F7; padding: 10px; font-size: 16px;")
        self.login_button.setFixedWidth(300)
        form_layout.addRow(self.login_button)

        self.invalid_input_label = QLabel("Invalid Username or Password")
        self.invalid_input_label.setStyleSheet("color: red; font-size: 14px;")
        self.invalid_input_label.setVisible(False)
        form_layout.addRow(self.invalid_input_label)

        main_layout.addLayout(form_layout)
        self.setLayout(main_layout)

    def switch_to_login(self):
        self.register_button.setText("Sign In")
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.login)

        self.login_button.setText("Don't have an account? Sign Up")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.switch_to_register)

    def switch_to_register(self):
        self.register_button.setText("Sign Up")
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.register)

        self.login_button.setText("Already have an account? Sign In")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.switch_to_login)

    def switch_to_chat(self):
        self.chat_window = ChatScreen(self.client_app)
        self.chat_window.show()
        self.close()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.client_app.send_message(f"REGISTER:{username}:{password}")
            response = self.client_app.receive_message()
            if response == "SUCCESSFUL":
                self.switch_to_chat()
            else:
                self.invalid_input_label.setVisible(True)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.client_app.send_message(f"LOGIN:{username}:{password}")
            response = self.client_app.receive_message()
            if response == "SUCCESSFUL":
                self.switch_to_chat()
            else:
                self.invalid_input_label.setVisible(True)
