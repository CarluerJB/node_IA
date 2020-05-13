# -*- coding: utf-8 -*-
"""
A module containing ``NodeEditorWidget`` class
"""
import os
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QGraphicsItem,
    QPushButton,
    QTextEdit,
)
from PyQt5.QtGui import QFont, QPen, QBrush, QColor
from PyQt5.QtCore import Qt

from nodeeditor.node.scene import Scene, InvalidFile
from nodeeditor.node.node import Node
from nodeeditor.node.edge import Edge, EDGE_TYPE_BEZIER
from nodeeditor.node.graphics_view import QDMGraphicsView

# import of all custom nodes
from nodeeditor.node.IANodes import (
    dense,
    concatenate,
    add,
    multiply,
    average,
    input,
    conv1d,
    conv2d,
    conv3d,
    depthwiseconv2d,
    activation,
    output,
    flatten,
    maximum,
    minimum,
    maxpooling1d,
    maxpooling2d,
    maxpooling3d,
    upsampling1d,
    upsampling2d,
    upsampling3d,
    globalmaxpooling1d,
    globalmaxpooling2d,
    globalmaxpooling3d,
    squeeze
)

from nodeeditor.node.IANodes.add import CustomNode_Add
from nodeeditor.node.IANodes.input import CustomNode_Input
from nodeeditor.node.IANodes.output import CustomNode_Output

#from nodeeditor.IA_input_node import CustomNode_Output


class NodeEditorWidget(QWidget):
    Scene_class = Scene

    """The ``NodeEditorWidget`` class"""

    def __init__(self, parent: QWidget = None):
        """
        :param parent: parent widget
        :type parent: ``QWidget``

        :Instance Attributes:

        - **filename** - currently graph's filename or ``None``
        """
        super().__init__(parent)

        self.filename = None
        self.codefilename = None

        self.initUI()

    def initUI(self):
        """Set up this ``NodeEditorWidget`` with its layout,  :class:`~nodeeditor.node.scene.Scene` and
        :class:`~nodeeditor.node.graphics_view.QDMGraphicsView`"""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # crate graphics scene
        self.scene = self.__class__.Scene_class()

        # create graphics view
        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

    def isModified(self) -> bool:
        """Has the `Scene` been modified?

        :return: ``True`` if the `Scene` has been modified
        :rtype: ``bool``
        """
        return self.scene.isModified()

    def isFilenameSet(self) -> bool:
        """Do we have graph loaded from file or new one?

        :return: ``True`` if filename is set. ``False`` if its a graph not saved to a file
        :rtype: ''bool''
        """
        return self.filename is not None

    def isCodeFilenameSet(self) -> bool:
        """Do we have graph loaded from Code file or new one?

        :return: ``True`` if codefilename is set. ``False`` if its a graph not saved to a code file
        :rtype: ''bool''
        """
        return self.codefilename is not None

    def getSelectedItems(self) -> list:
        """Shortcut returning `Scene`'s currently selected items

        :return: list of ``QGraphicsItems``
        :rtype: list[QGraphicsItem]
        """
        return self.scene.getSelectedItems()

    def hasSelectedItems(self) -> bool:
        """Is there something selected in the :class:`nodeeditor.node.scene.Scene`?

        :return: ``True`` if there is something selected in the `Scene`
        :rtype: ``bool``
        """
        return self.getSelectedItems() != []

    def canUndo(self) -> bool:
        """Can Undo be performed right now?

        :return: ``True`` if we can undo
        :rtype: ``bool``
        """
        return self.scene.history.canUndo()

    def canRedo(self) -> bool:
        """Can Redo be performed right now?

        :return: ``True`` if we can redo
        :rtype: ``bool``
        """
        return self.scene.history.canRedo()

    def getUserFriendlyFilename(self) -> str:
        """Get user friendly filename. Used in window title

        :return: just a base name of the file or `'New Graph'`
        :rtype: ``str``
        """
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    def fileNew(self):
        """Empty the scene (create new file)"""
        self.scene.clear()
        self.filename = None
        self.scene.history.clear()
        self.scene.history.storeInitialHistoryStamp()

    def fileLoad(self, filename: str):
        """Load serialized graph from JSON file

        :param filename: file to load
        :type filename: ``str``
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.scene.loadFromFile(filename)
            self.filename = filename
            self.scene.history.clear()
            self.scene.history.storeInitialHistoryStamp()
            return True
        except InvalidFile as e:
            print(e)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(
                self, "Error loading %s" % os.path.basename(filename), str(e)
            )
            return False
        finally:
            QApplication.restoreOverrideCursor()

    def fileSave(self, filename: str = None):
        """Save serialized graph to JSON file. When called with empty parameter, we won't store/remember the filename

        :param filename: file to store the graph
        :type filename: ``str``
        """
        if filename is not None:
            self.filename = filename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToFile(self.filename)
        QApplication.restoreOverrideCursor()
        return True

    def fileSaveToCode(self, codefilename: str = None):
        """Save graph to Code file. When called with empty parameter, we won't store/remember the codefilename

        :param codefilename: code file to store the graph
        :type codefilename: ``str``
        """
        if codefilename is not None:
            self.codefilename = codefilename
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.scene.saveToCodeFile(self.codefilename)
        QApplication.restoreOverrideCursor()
        return True

    def addNodes(self):
        """Testing method to create 3 `Nodes` with 3 `Edges` connecting them"""
        node1 = CustomNode_Input(self.scene)
        node2 = CustomNode_Input(self.scene)
        node3 = CustomNode_Add(self.scene)
        node4 = CustomNode_Output(self.scene)

        node1.setPos(-150, -150)
        node2.setPos(-150, 0)
        node3.setPos(200, -50)
        node4.setPos(500, -50)

        edge1 = Edge(self.scene, node1.outputs[0], node3.inputs[0], EDGE_TYPE_BEZIER)
        node1.onEdgeConnectionChanged(edge1)
        node3.onEdgeConnectionChanged(edge1)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[0], EDGE_TYPE_BEZIER)
        node2.onEdgeConnectionChanged(edge2)
        node3.onEdgeConnectionChanged(edge2)
        edge3 = Edge(self.scene, node3.outputs[0], node4.inputs[0], EDGE_TYPE_BEZIER)
        node3.onEdgeConnectionChanged(edge3)
        node4.onEdgeConnectionChanged(edge3)

        node1.evalImplementation()
        node2.evalImplementation()
        self.scene.history.storeInitialHistoryStamp()

    def addCustomNode(self):
        """Testing method to create a custom Node with custom content"""
        from nodeeditor.node.content_widget import QDMNodeContentWidget
        from nodeeditor.node.serializable import Serializable

        class NNodeContent(QLabel):  # , Serializable):
            def __init__(self, node, parent=None):
                super().__init__("FooBar")
                self.node = node
                self.setParent(parent)

        class NNode(Node):
            NodeContent_class = NNodeContent

        self.scene.setNodeClassSelector(lambda data: NNode)
        node = NNode(self.scene, "A Custom Node 1", inputs=[0, 1, 2])

        print("node content:", node.content)

    def addDebugContent(self):
        """Testing method to put random QGraphicsItems and elements into QGraphicsScene"""
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my Awesome text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
