import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import cv2

from algorithms.binarization import(
    histogram,
    otsu
)

class Slider(QWidget):

    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)

        layout = QVBoxLayout()

        self.label = QLabel(f"Current value: {128}")
        # self.label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label)

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(128)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(256)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_change)
        self.slider.setOrientation(Qt.Horizontal)
        layout.addWidget(self.slider)

        self.setLayout(layout)
        self.setWindowTitle("Slider Test")

    def slider_value_change(self):
        threshold = self.slider.value()
        self.label.setText(f"Current value: {threshold}")


class ImageListViewer(QWidget):

    sendPath = pyqtSignal(str)

    def __init__(self):
        super(ImageListViewer, self).__init__()

        layout = QVBoxLayout()

        # self.listview = QListView()
        # self.listview.setViewMode(QListView.IconMode)
        self.listwidget = QListWidget()
        self.listwidget.setViewMode(QListView.IconMode)
        self.listwidget.setIconSize(QSize(64, 64))

        layout.addWidget(self.listwidget)
        # layout.addWidget(self.listview)

        _fromUtf8 = lambda s: s

        files = []

        self.image_dir = os.path.join(
             "C:" + os.sep, "Users", "Zhenya", "image-processing-and-recognition",
            "image_binarization", "examples"
        )
        for file in os.listdir(self.image_dir):
            files.append(os.path.join(self.image_dir, file))

        for x in files:
            item = QListWidgetItem()
            icon = QIcon()
            icon.addPixmap(QPixmap(_fromUtf8(x)), QIcon.Normal, QIcon.Off)
            item.setIcon(icon)
            item.setText(x.split("\\")[-1])
            self.listwidget.addItem(item)

        self.listwidget.itemDoubleClicked.connect(self.double_click)
        self.setLayout(layout)

    def double_click(self, item):
        filename = item.text()
        filename = os.path.join(self.image_dir, filename)
        print(filename)
        self.sendPath.emit(filename)


class Histogram(QWidget):

    def __init__(self):
        super(Histogram, self).__init__()

        self.hist_widget = pg.HistogramLUT

    @pyqtSlot(str)
    def plot_histogram(self, path):
        print(path)
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = histogram(image)
        print(hist)
        self.hist_widget.plot(range(len(hist)), hist)


# app = QApplication(sys.argv)
# ex = ImageListViewer()
# ex.show()
# sys.exit(app.exec_())