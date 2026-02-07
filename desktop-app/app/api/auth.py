def login(self):
    response = requests.post(
        f"{API_BASE_URL}/login/",
        data={
            "username": self.username.text(),
            "password": self.password.text()
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code == 200:
        self.token = response.json().get("token")
        self.accept()
    else:
        QMessageBox.warning(
            self,
            "Login Failed",
            response.text
        )
