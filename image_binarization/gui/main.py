import sys

from PyQt5.QtWidgets import *

from widgets import (
    Slider, ImageListViewer,
    Histogram, ImageGrid
)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Image Binarization")

        layout = QVBoxLayout()

        self.slider = Slider()
        self.viewer = ImageListViewer()
        self.hist = Histogram()
        self.im_grid = ImageGrid()

        self.viewer.sendPath.connect(self.hist.plot_histogram)
        self.viewer.sendPath.connect(self.im_grid.set_images)
        self.im_grid.sendOtsu.connect(self.hist.plot_threshold)
        self.slider.sendThreshold.connect(self.im_grid.update_manual)

        layout.addWidget(self.slider)
        layout.addWidget(self.hist)
        layout.addWidget(self.im_grid)
        layout.addWidget(self.viewer)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.showMaximized()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
