import cv2
import numpy as np

class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.current_image = None

    def load_image(self, path):
        self.original_image = cv2.imread(path)
        self.current_image = self.original_image.copy()
        return self.current_image

    def apply_brightness_contrast(self, brightness=0, contrast=0):
        img = self.original_image.copy()
        brightness = int((brightness - 50) * 2.55)
        contrast = int((contrast - 50) * 2.55)
        self.current_image = cv2.convertScaleAbs(img, alpha=1 + contrast / 127., beta=brightness)
        return self.current_image

    def apply_filter(self, filter_name):
        img = self.current_image.copy()
        if filter_name == "grayscale":
            self.current_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif filter_name == "canny":
            self.current_image = cv2.Canny(img, 100, 200)
        elif filter_name == "gaussian":
            self.current_image = cv2.GaussianBlur(img, (5, 5), 0)
        elif filter_name == "median":
            self.current_image = cv2.medianBlur(img, 5)
        elif filter_name == "sobel":
            self.current_image = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
        elif filter_name == "thresholding":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, self.current_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        elif filter_name == "imagerotation":
            self.current_image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif filter_name == "imageresizing":
            self.current_image = cv2.resize(img, (200, 200))
        elif filter_name == "erosion":
            kernel = np.ones((5, 5), np.uint8)
            self.current_image = cv2.erode(img, kernel, iterations=1)
        elif filter_name == "dilation":
            kernel = np.ones((5, 5), np.uint8)
            self.current_image = cv2.dilate(img, kernel, iterations=1)
        elif filter_name == "flipH":
            self.current_image = cv2.flip(img, 1)
        elif filter_name == "flipV":
            self.current_image = cv2.flip(img, 0)
        return self.current_image

    def reset(self):
        self.current_image = self.original_image.copy()
        return self.current_image

    def save_image(self, path):
        cv2.imwrite(path, self.current_image)
