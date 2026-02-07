# from PyQt5.QtWidgets import (
#     QWidget, QVBoxLayout, QListWidget, QListWidgetItem
# )
# from PyQt5.QtCore import Qt

# class HistoryWidget(QWidget):
#     def __init__(self, api_client, on_select_callback):
#         super().__init__()
#         self.api = api_client
#         self.on_select = on_select_callback

#         layout = QVBoxLayout()
#         self.list_widget = QListWidget()
#         self.list_widget.itemClicked.connect(self.load_dataset)

#         layout.addWidget(self.list_widget)
#         self.setLayout(layout)

#     def refresh(self):
#         self.list_widget.clear()
#         datasets = self.api.get_history()

#         for ds in datasets:
#             item = QListWidgetItem(
#                 f"{ds['filename']}  |  {ds['uploaded_at']}"
#             )
#             item.setData(Qt.UserRole, ds["id"])
#             self.list_widget.addItem(item)

#     def load_dataset(self, item):
#         dataset_id = item.data(Qt.UserRole)
#         data = self.api.get_summary(dataset_id)
#         self.on_select(data)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget
from PyQt5.QtCore import Qt

class HistoryWidget(QWidget):
    def __init__(self, api, on_select):
        super().__init__()
        self.api = api
        self.on_select = on_select

        self.list = QListWidget()
        self.list.itemClicked.connect(self.load_dataset)

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        self.setLayout(layout)

    def refresh(self):
        self.list.clear()
        datasets = self.api.get_history().json()

        for ds in datasets:
            text = f"{ds['filename']} ({ds['uploaded_at']})"
            self.list.addItem(text)


    def load_dataset(self, item):
        dataset_id = int(item.text().split(" - ")[0])
        response = self.api.get_summary(dataset_id)
        self.on_select(response.json())
