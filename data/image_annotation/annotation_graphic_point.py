from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QRectF

"""Appearance of point element"""
class Graphic_point(QGraphicsItem):
    def __init__(self, point, parent=None):
        super().__init__(parent)
        self.point = point
        self.point_width = 0.25
        self.size=1
        self.point_color = QColor("#F9CB40")
        self.point_pen = QPen(self.point_color)
        self.point_pen.setWidth(self.point_width)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setPen(self.point_pen)
        painter.drawRect(0, 0, self.size, self.size)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.point_width,
            self.point_width
        ).normalized()
