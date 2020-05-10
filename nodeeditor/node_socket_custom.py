from nodeeditor.node_graphics_socket import QDMGraphicsSocket
from nodeeditor.node_socket import Socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CustomGraphicsSocket(QDMGraphicsSocket):
    def initAssets(self):
        # determine socket color
        self._color_background = QColor("#606060")
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        self.Ellipse = QRectF(
            -self.radius, -self.radius, 2 * self.radius, 2 * self.radius
        )
        self.VLine = QLine(0, -self.radius / 2, 0, self.radius / 2)
        self.HLine = QLine(-self.radius / 2, 0, self.radius / 2, 0)
        Painted_Ellipse = painter.drawEllipse(self.Ellipse)
        Painted_Symbol = painter.drawLine(self.VLine)
        Painted_Symbol = painter.drawLine(self.HLine)


class CustomSocket(Socket):
    def initInnerClasses(self):
        self.grSocket = CustomGraphicsSocket(self)

    def initSetting(self):
        self.isAddSocket = True
