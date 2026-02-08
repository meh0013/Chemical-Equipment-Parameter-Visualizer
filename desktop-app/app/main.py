import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QDialog, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

from ui.main_window import MainWindow
from api.client import APIClient
from utils.config import API_BASE_URL


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.token = None
        self.access_token = None

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Login")
        btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(btn)
        self.setLayout(layout)

    def login(self):
        response = requests.post(
            f"{API_BASE_URL}/token/",
            json={
                "username": self.username.text(),
                "password": self.password.text()
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data["access"]
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid username or password"
            )


def main():
    app = QApplication(sys.argv)

    login = LoginDialog()
    if login.exec_() != QDialog.Accepted:
        sys.exit(0)

    api = APIClient(login.access_token)
    window = MainWindow(api)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

