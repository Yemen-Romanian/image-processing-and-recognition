# Only needed for access to command line arguments
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from widgets import Slider, ImageListViewer, Histogram


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Image Binarization")

        layout = QVBoxLayout()

        self.slider = Slider()
        self.viewer = ImageListViewer()
        self.hist = Histogram()

        self.viewer.sendPath.connect(self.hist.plot_histogram)
        layout.addWidget(self.slider)
        layout.addWidget(self.hist)
        layout.addWidget(self.viewer)
        self.viewer.resize(100, 300)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.showMaximized()


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()


# Your application won't reach here until you exit and the event 
# loop has stopped.
