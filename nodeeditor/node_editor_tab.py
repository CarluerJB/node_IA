import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_drag_list import NodeDragList


class NodeEditorTabs(QWidget):
    NodeEditorWidget_class = NodeEditorWidget
    def __init__(self, parent):
        super().__init__(parent)
        self.initUi()
    
    def initUi(self):
        self.nodeEditor = self.__class__.NodeEditorWidget_class(self)
        self.node_drag_list = NodeDragList(self)
        self.hbox = QHBoxLayout(self)
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.nodeEditor)
        self.splitter1.addWidget(self.node_drag_list)
        self.hbox.addWidget(self.splitter1)
        self.setLayout(self.hbox)