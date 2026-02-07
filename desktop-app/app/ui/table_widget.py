from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class EquipmentTable(QTableWidget):
    def load_data(self, data):
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))

        self.setHorizontalHeaderLabels(data[0].keys())

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row.values()):
                self.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(value))
                )
