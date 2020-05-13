from PyQt5.QtGui import QColor, QPen, QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from annotation_point import point

MODE_POINT = 1
MODE_LINE = 2
MODE_CIRCLE = 3

# Current view of the scene
class QDMGraphicsView(QGraphicsView):

    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene

        self.initUI()

        self.setScene(self.grScene)
        self._color_point = QColor("#F9CB40")
        self.pen_point = QPen(self._color_point)
        self.pen_point.setWidth(1)
        self._color_segment = QColor("#FF715B")
        self.pen_segment = QPen(self._color_segment)
        self.pen_segment.setWidth(1)

        self.mode = MODE_POINT

        self.zoomInFactor = 1.25
        # SET zomm clamp to False to enable infinite zoom
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]


    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)




    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        # check if click is on image
        if isinstance(item, QGraphicsPixmapItem):
            if self.mode==MODE_POINT:
                clicked_point = point(self.grScene.scene)
                pos = self.mapToScene(event.pos())
                clicked_point.setPos(int(pos.x()), int(pos.y()))
        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)
        pass

    def rightMouseButtonPress(self, event):
        # TO REMOVE ! TEST FOR POINT SAVE
        self.grScene.scene.set_next_image()
        super().mousePressEvent(event)
        pass

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)
        pass

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)


    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
