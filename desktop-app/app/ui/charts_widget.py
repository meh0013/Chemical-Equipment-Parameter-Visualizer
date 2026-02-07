from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class ChartWidget(FigureCanvasQTAgg):
    def __init__(self):
        self.figure = Figure()
        super().__init__(self.figure)

    def plot_equipment_types(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(distribution.keys(), distribution.values())
        ax.set_title("Equipment Type Distribution")
        self.draw()
