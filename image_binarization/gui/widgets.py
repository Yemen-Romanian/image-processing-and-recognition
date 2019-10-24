import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

from algorithms.binarization import(
    histogram,
    otsu,
    get_grayscale
)


class Slider(QWidget):
    sendThreshold = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.label = QLabel(f"Current value: {128}")
        layout.addWidget(self.label)

        self.slider = QSlider()
        self.slider.setFixedWidth(1470)
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setValue(128)
        self.slider.setSingleStep(1)
        self.slider.setTickInterval(256)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.slider_value_change)
        self.slider.valueChanged.connect(self.update_label)
        self.slider.setOrientation(Qt.Horizontal)
        layout.addWidget(self.slider, Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle("Slider Test")

    def slider_value_change(self):
        threshold = self.slider.value()
        self.sendThreshold.emit(str(threshold))

    def update_label(self):
        self.label.setText(f"Current value: {self.slider.value()}")


class ImageListViewer(QWidget):

    sendPath = pyqtSignal(str)

    def __init__(self):
        super(ImageListViewer, self).__init__()

        layout = QVBoxLayout()

        self.listwidget = QListWidget()
        self.listwidget.setViewMode(QListView.IconMode)
        self.listwidget.setIconSize(QSize(64, 64))

        layout.addWidget(self.listwidget)

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
        self.sendPath.emit(filename)


class Histogram(QWidget):

    def __init__(self):
        super(Histogram, self).__init__()

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.sumbu1 = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)


    @pyqtSlot(str)
    def plot_histogram(self, path):
        self.path = path
        image = cv2.imread(path)
        if len(image.shape) > 2:
            image = get_grayscale(image)
        hist = histogram(image)

        self.canvas.sumbu1.clear()
        self.canvas.sumbu1.plot(hist, color='red', linewidth=3.0)
        self.canvas.sumbu1.set_title('Histogram')
        self.canvas.sumbu1.grid()

        self.canvas.draw()

    @pyqtSlot(str)
    def plot_threshold(self, margin):
        self.canvas.sumbu1.axvline(x=int(margin))
        self.canvas.draw()


class ImageGrid(QWidget):
    sendOtsu = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ImageGrid, self).__init__(parent)

        self.grid = FigureCanvas(Figure())
        self.grid.original_image = self.grid.figure.add_subplot(131)
        self.grid.original_image.set_title("Original image")
        self.grid.manual_image = self.grid.figure.add_subplot(132)
        self.grid.manual_image.set_title("Manual threshold")
        self.grid.otsu_image = self.grid.figure.add_subplot(133)
        self.grid.otsu_image.set_title("Otsu threshold")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.grid)

        self.setLayout(self.layout)

    def set_images(self, path):
        image = cv2.imread(path)
        if len(image.shape) > 2:
            image = get_grayscale(image)
        self.image = image
        otsu_threshold = otsu(histogram(image))
        otsu_image = image > otsu_threshold
        self.grid.original_image.imshow(image, cmap='gray')
        self.grid.manual_image.imshow(image, cmap='gray')
        self.grid.otsu_image.imshow(otsu_image, cmap='gray')
        self.grid.draw()

        self.sendOtsu.emit(str(otsu_threshold))

    def update_manual(self, threshold):
        try:
            self.grid.manual_image.clear()
            self.grid.manual_image.imshow(self.image > int(threshold), cmap='gray')
            self.grid.manual_image.set_title("Manual threshold")
            self.grid.draw()
        except:
            pass
