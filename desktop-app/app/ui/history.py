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
