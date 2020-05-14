from PyQt5.QtGui import QPixmap

class Image():
    def __init__(self, image):
        self.pixmap = QPixmap(image)
        self.points = []

    def addPoint(self, point):
        self.points.append(point)
