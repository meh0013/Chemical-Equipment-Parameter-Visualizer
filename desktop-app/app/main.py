# import sys
# from PyQt5.QtWidgets import QApplication
# from app.ui.main_window import MainWindow
# from app.api.client import APIClient

# app = QApplication(sys.argv)
# api = APIClient(token="YOUR_TOKEN")

# from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout

# class LoginDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Login")

#         self.username = QLineEdit()
#         self.password = QLineEdit()
#         self.password.setEchoMode(QLineEdit.Password)

#         btn = QPushButton("Login")
#         btn.clicked.connect(self.accept)

#         layout = QVBoxLayout()
#         layout.addWidget(self.username)
#         layout.addWidget(self.password)
#         layout.addWidget(btn)

#         self.setLayout(layout)


# window = MainWindow(api)
# window.show()
# sys.exit(app.exec_())

#---------------------------------------------------------------------------------------------------------------------------------

# import sys
# import requests
# from PyQt5.QtWidgets import (
#     QApplication, QDialog, QLineEdit,
#     QPushButton, QVBoxLayout, QMessageBox
# )

# from app.ui.main_window import MainWindow
# from app.api.client import APIClient
# from app.utils.config import API_BASE_URL

# # -------------------------
# # Login Dialog
# # -------------------------

# class LoginDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Login")

#         self.token = None

#         self.username = QLineEdit()
#         self.username.setPlaceholderText("Username")

#         self.password = QLineEdit()
#         self.password.setPlaceholderText("Password")
#         self.password.setEchoMode(QLineEdit.Password)

#         login_btn = QPushButton("Login")
#         login_btn.clicked.connect(self.authenticate)

#         layout = QVBoxLayout()
#         layout.addWidget(self.username)
#         layout.addWidget(self.password)
#         layout.addWidget(login_btn)

#         self.setLayout(layout)

#     def authenticate(self):
#         try:
#             response = requests.post(
#                 f"{API_BASE_URL}/login/",
#                 data={
#                     "username": self.username.text(),
#                     "password": self.password.text()
#                 }
#             )

#             if response.status_code == 200:
#                 self.token = response.json().get("token")
#                 if self.token:
#                     self.accept()
#                     return

#             QMessageBox.warning(
#                 self,
#                 "Login Failed",
#                 "Invalid username or password"
#             )

#         except Exception as e:
#             QMessageBox.critical(
#                 self,
#                 "Error",
#                 f"Cannot reach server:\n{str(e)}"
#             )


# # -------------------------
# # App Entry Point
# # -------------------------

# def main():
#     app = QApplication(sys.argv)

#     login = LoginDialog()
#     if login.exec_() != QDialog.Accepted:
#         sys.exit(0)

#     api = APIClient(token=login.token)

#     window = MainWindow(api)
#     window.show()

#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()

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

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

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

