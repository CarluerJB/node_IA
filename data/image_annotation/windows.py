from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math
from data.image_annotation.scene import ImageScene
from data.image_annotation.Graphics import QDMGraphicsView



class AnnotationEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.name_company = 'Bionomy'
        self.name_product = 'AnnotationEditor'
        self.initUI()

    def initUI(self):
        self.annotationTool = AnnotationTool(self)
        self.setCentralWidget(self.annotationTool)
        self.show()

class AnnotationTool(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        annotation_tool_box = AnnotationToolBox()
        self.scene = ImageScene()
        self.view = QDMGraphicsView(self.scene.grScene, self)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(annotation_tool_box)
        splitter1.addWidget(self.view)
        splitter1.setSizes([100,200])

        hbox.addWidget(splitter1)

        self.setLayout(hbox)


class ClickableLabel(QLabel):
    """
        A Label that emits a signal when clicked.
    """

    clicShow = pyqtSignal()
    clicHide = pyqtSignal()
    def __init__(self, text):
        super().__init__(text)
        self.init_text = text
        self.clic = False
        self.setText("+ " + self.init_text)

    def mousePressEvent(self, event):
        if self.clic:
            self.setText("+ " + self.init_text)
            self.clicHide.emit()
            print(self.text())
            self.clic = False
        else:
            self.setText("- " + self.init_text)
            self.clicShow.emit()
            self.clic = True

class AnnotationToolBox(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.rShape = ClickableLabel("Region Shape")
        self.layout.addWidget(self.rShape)

        self.shape_widget = ShapeWidget()

        self.layout.addWidget(self.shape_widget)
        self.shape_widget.hide()
        self.rShape.clicShow.connect(self.shape_widget.show)
        self.rShape.clicHide.connect(self.shape_widget.hide)

        self.project = ClickableLabel("Project")
        self.layout.addWidget(self.project)

        self.setLayout(self.layout)

class ShapeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.Circle = QLabel("Circle")
        self.Point = QLabel("Point")
        self.Cube = QLabel("Cube")
        self.layout.addWidget(self.Circle)
        self.layout.addWidget(self.Point)
        self.layout.addWidget(self.Cube)
        self.setLayout(self.layout)

    def hide(self):
        self.Circle.hide()
        self.Point.hide()
        self.Cube.hide()

    def show(self):
        self.Circle.show()
        self.Point.show()
        self.Cube.show()
