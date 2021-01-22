import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def get_images(folder):
    VALID_FORMAT = ('.BMP', '.GIF', '.JPG', '.JPEG', '.PNG', '.PBM', '.PGM', '.PPM', '.TIFF', '.XBM')
    image_list = []
    if os.path.isdir(folder):
        for file in os.listdir(folder):
            if file.upper().endswith(VALID_FORMAT):
                im_path = os.path.join(folder, file)
                image_obj = {'name': file, 'path': im_path}
                image_list.append(image_obj)
    return image_list


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.imageId = 0
        self.listOfImages = []

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setGeometry(150, 60, 200, 30)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.valueChanged.connect(self.update_slider)

        button_action_open = QAction(QIcon("buttons/open.png"), "Open", self)
        button_action_open.triggered.connect(self.open_folder)

        button_action_close = QAction(QIcon("buttons/close.png"), "Close", self)
        button_action_close.triggered.connect(self.close_folder)

        button_action_left = QAction(QIcon("buttons/left.png"), "Left", self)
        button_action_left.triggered.connect(self.id_to_left)

        button_action_right = QAction(QIcon("buttons/right.png"), "Right", self)
        button_action_right.triggered.connect(self.id_to_right)

        tb = self.addToolBar("Open")
        tb.addAction(button_action_close)
        tb.addAction(button_action_left)
        tb.addAction(button_action_open)
        tb.addAction(button_action_right)

        self.label = QLabel(self)
        self.pixmap = QPixmap("buttons/no.png")
        self.pixmap = self.pixmap.scaledToWidth(300)
        self.pixmap = self.pixmap.scaledToHeight(300)
        self.label.setPixmap(self.pixmap)
        self.label.setGeometry(100, 100, 300, 300)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Image Viewer v. 0.1')
        self.show()

    def open_image(self):
        self.pixmap = QPixmap(self.listOfImages[self.imageId].get("path"))
        self.pixmap = self.pixmap.scaledToWidth(300)
        self.pixmap = self.pixmap.scaledToHeight(300)
        self.label.setPixmap(self.pixmap)
        self.sld.setValue(self.imageId)

    def open_folder(self):
        self.dir = QFileDialog.getExistingDirectory(self, 'Open folder')
        self.listOfImages = get_images(self.dir)
        print(len(self.listOfImages) - 1)
        self.sld.setRange(0, len(self.listOfImages) - 1)
        self.open_image()
        self.sld.setValue(self.imageId)

    def id_to_left(self):
        if self.imageId > 0:
            self.imageId -= 1
            self.open_image()
            self.sld.setValue(self.imageId)

    def id_to_right(self):
        if self.imageId < len(self.listOfImages) - 1:
            self.imageId += 1
            self.open_image()
            self.sld.setValue(self.imageId)

    def close_folder(self):
        if len(self.listOfImages) > 0:
            self.pixmap = QPixmap("buttons/no.png")
            self.pixmap = self.pixmap.scaledToWidth(300)
            self.pixmap = self.pixmap.scaledToHeight(300)
            self.label.setPixmap(self.pixmap)
            self.listOfImages.clear()
            self.imageId = 0
            self.sld.setValue(0)

    def update_slider(self):
        if len(self.listOfImages) > 0:
            self.imageId = self.sld.value()
            self.open_image()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
