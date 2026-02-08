from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QFileDialog, QListWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.setWindowTitle("Chemical Equipment Analyzer")
        # Main Window 
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        central.setLayout(main_layout)

        # Top bar - Upper Section 
        top_bar = QHBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setFixedSize(120, 28)
        self.upload_btn.clicked.connect(self.upload_csv)

        top_bar.addWidget(self.upload_btn)
        top_bar.addStretch()

        main_layout.addLayout(top_bar)

        # Summary Section 
        self.summary_label = QLabel("Upload a CSV file to view summary")
        self.summary_label.setStyleSheet(
            "font-size: 13px; font-weight: bold; padding: 4px;"
        )
        main_layout.addWidget(self.summary_label)

        # Main Content Layout 
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout, stretch=1)

        # Table Section 
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.table, stretch=4)

        # Chart Section
        chart_panel = QVBoxLayout()
        chart_panel.setSpacing(6)
        content_layout.addLayout(chart_panel, stretch=2)

        self.flow_canvas = self._create_chart(chart_panel)
        self.pressure_canvas = self._create_chart(chart_panel)
        self.temp_canvas = self._create_chart(chart_panel)

        # Bottom Bar - Lower Section 
        bottom_bar = QHBoxLayout()

        # History Section 
        history_layout = QVBoxLayout()
        history_label = QLabel("History (Last 5 uploads)")
        history_label.setStyleSheet("font-weight: bold;")

        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(90)

        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)

        bottom_bar.addLayout(history_layout, stretch=4)

        # PDF Button 
        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.setFixedSize(140, 32)
        self.pdf_btn.clicked.connect(self.download_pdf)

        bottom_bar.addWidget(self.pdf_btn, alignment=Qt.AlignBottom)

        main_layout.addLayout(bottom_bar)

        self.refresh_history()
        self.showMaximized()

    # Helper Functions
    def _create_chart(self, layout):
        fig = Figure(figsize=(3, 2))
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(180)
        layout.addWidget(canvas)
        return canvas

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        response = self.api.upload_csv(file_path)
        if response.status_code == 200:
            self.update_view(response.json())
            self.refresh_history()

    def update_view(self, data):
        # summary = data["summary"]
        self.current_summary = data["summary"] 
        summary = self.current_summary
        table_data = data["table"]

        self.summary_label.setText(
            f"Total: {summary['total_equipment']} | "
            f"Avg Flowrate: {summary['average_flowrate']:.2f} | "
            f"Avg Pressure: {summary['average_pressure']:.2f} | "
            f"Avg Temp: {summary['average_temperature']:.2f}"
        )

        self.populate_table(table_data)

        self.plot_average(self.flow_canvas, "Avg Flowrate", summary["average_flowrate"])
        self.plot_average(self.pressure_canvas, "Avg Pressure", summary["average_pressure"])
        self.plot_average(self.temp_canvas, "Avg Temperature", summary["average_temperature"])

    def populate_table(self, rows):
        headers = list(rows[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            for c, key in enumerate(headers):
                self.table.setItem(r, c, QTableWidgetItem(str(row[key])))

        self.table.resizeColumnsToContents()

    def plot_average(self, canvas, title, value):
        fig = canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)

        ax.bar([title], [value])
        ax.set_ylim(bottom=0)
        ax.set_title(title, fontsize=10)

        ax.text(0, value, f"{value:.2f}", ha="center", va="bottom", fontsize=9)

        fig.tight_layout()
        canvas.draw()

    def refresh_history(self):
        self.history_list.clear()
        response = self.api.get_history()
        if response.status_code == 200:
            for item in response.json():
                self.history_list.addItem(item["filename"])

    def download_pdf(self):
        if not hasattr(self, "current_summary"):
            print("No data available yet")
            return

        response = self.api.download_pdf(self.current_summary)

        if response.status_code == 200:
            path = "equipment_report.pdf"
            with open(path, "wb") as f:
                f.write(response.content)
            os.startfile(path)
        else:
            print("PDF download failed:", response.text)

