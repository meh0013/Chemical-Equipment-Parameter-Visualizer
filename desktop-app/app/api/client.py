# import requests

# BASE_URL = "http://127.0.0.1:8000/api"

# class APIClient:
#     def __init__(self, token=None):
#         self.session = requests.Session()
#         if token:
#             self.session.headers.update({
#                 "Authorization": f"Token {token}"
#             })

#     def upload_csv(self, file_path):
#         with open(file_path, "rb") as f:
#             files = {"file": f}
#             return self.session.post(f"{BASE_URL}/upload/", files=files).json()

#     def get_summary(self, dataset_id):
#         return self.session.get(
#             f"{BASE_URL}/summary/{dataset_id}/"
#         ).json()

#     def get_history(self):
#         return self.session.get(
#             f"{BASE_URL}/history/"
#         ).json()

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

    def get_summary(self, dataset_id):
        return self.session.get(
            f"{API_BASE_URL}/summary/{dataset_id}/"
        )

