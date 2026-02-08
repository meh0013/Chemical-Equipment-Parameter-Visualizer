import requests
from utils.config import API_BASE_URL

class APIClient:
    def __init__(self, access_token):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

    def upload_csv(self, file_path):
        with open(file_path, "rb") as f:
            return self.session.post(
                f"{API_BASE_URL}/upload/",
                files={"file": f}
            )

    def get_history(self):
        return self.session.get(
            f"{API_BASE_URL}/history/"
        )

    def download_pdf(self, summary):
        return self.session.post(
            f"{API_BASE_URL}/pdf/",
            json={"summary": summary},
        )


