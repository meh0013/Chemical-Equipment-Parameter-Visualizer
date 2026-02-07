# from PyQt5.QtWidgets import QHBoxLayout
# from app.ui.history import HistoryWidget
# from app.ui.table_widget import EquipmentTable
# from app.ui.charts_widget import ChartWidget

# class MainWindow(QMainWindow):
#     def __init__(self, api):
#         super().__init__()
#         self.api = api

#         central = QWidget()
#         layout = QHBoxLayout()

#         self.history = HistoryWidget(api, self.display_dataset)
#         self.table = EquipmentTable()
#         self.chart = ChartWidget()

#         layout.addWidget(self.history, 1)
#         layout.addWidget(self.table, 3)
#         layout.addWidget(self.chart, 3)

#         central.setLayout(layout)
#         self.setCentralWidget(central)

#         self.history.refresh()

#     def display_dataset(self, data):
#         self.table.load_data(data["rows"])
#         self.chart.plot_equipment_types(
#             data["type_distribution"]
#         )

#     def download_report(self, dataset_id):
#     response = self.api.session.get(
#         f"{API_BASE_URL}/report/{dataset_id}/",
#         stream=True
#     )
#     with open("report.pdf", "wb") as f:
#         for chunk in response.iter_content(1024):
#             f.write(chunk)

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QFileDialog, QTextEdit
)
from ui.history import HistoryWidget

class MainWindow(QMainWindow):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Equipment Analyzer")
        self.resize(1200, 800)
        self.show()

        central = QWidget()
        layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.history = HistoryWidget(api, self.display_dataset)

        layout.addWidget(self.upload_btn)
        layout.addWidget(self.history)
        layout.addWidget(self.output)

        central.setLayout(layout)
        self.setCentralWidget(central)

        self.history.refresh()

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if file_path:
            response = self.api.upload_csv(file_path)
            self.output.setText(response.text)
            self.history.refresh()

    def display_dataset(self, data):
        self.output.setText(str(data))
