import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from cam_logic import ImageProcessor

class ImageEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImageEditor, self).__init__()
        uic.loadUi('gui.ui', self)

        self.processor = ImageProcessor()
        self.image = None

        ### call from logic ###


        self.uploadimage.clicked.connect(self.upload_image)

        self.grayscale.clicked.connect(lambda: self.apply_filter("grayscale"))
        self.gaussian.clicked.connect(lambda: self.apply_filter("gaussian"))
        self.median.clicked.connect(lambda: self.apply_filter("median"))
        self.sobel.clicked.connect(lambda: self.apply_filter("sobel"))
        self.canny.clicked.connect(lambda: self.apply_filter("canny"))
        self.thresholding.clicked.connect(lambda: self.apply_filter("thresholding"))
        self.imagerotation.clicked.connect(lambda: self.apply_filter("imagerotation"))
        self.imageresizing.clicked.connect(lambda: self.apply_filter("imageresizing"))
        self.erosion.clicked.connect(lambda: self.apply_filter("erosion"))
        self.dilation.clicked.connect(lambda: self.apply_filter("dilation"))
        self.flipH.clicked.connect(lambda: self.apply_filter("flipH"))
        self.flipV.clicked.connect(lambda: self.apply_filter("flipV"))

        self.brightness.valueChanged.connect(self.update_brightness_contrast)
        self.contrast.valueChanged.connect(self.update_brightness_contrast)

        self.save.clicked.connect(self.save_image)
        self.reset.clicked.connect(self.reset_image)

    def upload_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if filename:
            img = self.processor.load_image(filename)
            self.display_image(img)

    def display_image(self, img):
        if img is None:
            return
        if len(img.shape) == 2:
            qformat = QImage.Format_Grayscale8
            h, w = img.shape
            qt_img = QImage(img.data, w, h, w, qformat)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = img_rgb.shape
            bytes_per_line = ch * w
            qt_img = QImage(img_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        self.imagelabel.setPixmap(pixmap)

    def apply_filter(self, filter_name):
        img = self.processor.apply_filter(filter_name)

        # Convert float images to 8-bit for display compatibility
        if img is not None and (img.dtype == np.float32 or img.dtype == np.float64):
            img = cv2.convertScaleAbs(img)

        self.display_image(img)

    def update_brightness_contrast(self):
        brightness = self.brightness.value()
        contrast = self.contrast.value()
        img = self.processor.apply_brightness_contrast(brightness, contrast)
        self.display_image(img)

    def reset_image(self):
        img = self.processor.reset()
        self.display_image(img)

    def save_image(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if filename:
            self.processor.save_image(filename)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec_())
