from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor, QPen

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.image = scene.image
        self.addItem(self.image)

        # settings
        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)
        # self.pixmap = QGraphicsPixmapItem()
        # self.addItem(self.pixmap)

        self.setBackgroundBrush(self._color_background)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    # def set_image(self, image='le_parrain.jpg'):
    #     img = QPixmap(image)
    #     self.pixmap.setPixmap(img)
