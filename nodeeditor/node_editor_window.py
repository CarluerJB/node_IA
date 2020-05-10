# -*- coding: utf-8 -*-
"""
A module containing Main Window class
"""
import os
import json
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_content_conf import *
from nodeeditor.project_tab import ProjectTabs
from nodeeditor.node_node_custom import CustomNode, CustomContent
from nodeeditor.utils import dumpException
from nodeeditor.IA_input_node import *
from nodeeditor.node_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER


class NodeEditorWindow(QMainWindow):
    NodeEditorWidget_class = NodeEditorWidget

    """Class representing NodeEditor's Main Window"""

    def __init__(self):
        """
        :Instance Attributes:

        - **name_company** - name of the company, used for permanent profile settings
        - **name_product** - name of this App, used for permanent profile settings
        """
        super().__init__()

        self.name_company = "Bionomy"
        self.name_product = "NodeEditor"

        self.initUI()

    def initUI(self):
        """Set up this ``QMainWindow``. Create :class:`~nodeeditor.node_editor_widget.NodeEditorWidget`, Actions and Menus"""
        self.createActions()
        self.createMenus()

        # create node editor widget
        self.tabs_project = ProjectTabs(self)
        self.tabs_project.model_tab.nodeEditor.scene.addHasBeenModifiedListener(
            self.setTitle
        )
        self.tabs_project.model_tab.nodeEditor.scene.addDragEnterListener(
            self.onDragEnter
        )
        self.tabs_project.model_tab.nodeEditor.scene.addDropListener(self.onDrop)
        self.tabs_project.model_tab.nodeEditor.scene.setNodeClassSelector(
            self.getNodeClassFromData
        )
        self.setCentralWidget(self.tabs_project)
        self.createStatusBar()
        self.scene = self.tabs_project.model_tab.nodeEditor.scene

        # set window properties
        self.setGeometry(200, 200, 1600, 600)
        self.setTitle()
        # self.showMaximized()
        self.show()

    def contextMenuEvent(self, event):

        try:
            item = self.scene.getView().getItemAtClick(event)
            print(event.pos())
            print(item)
            if type(item) == QGraphicsProxyWidget:
                item = item.widget()
            if hasattr(item, "node") or hasattr(item, "socket"):
                self.handleNodeContextMenu(event)
            elif hasattr(item, "edge"):
                self.handleEdgeContextMenu(event)
            else:
                self.handleNewNodeContextMenu(event)
            return super().contextMenuEvent(event)
        except Exception as e:
            dumpException(e)

    def handleNodeContextMenu(self, event):
        print("CONTEXT : NODE")

    def handleEdgeContextMenu(self, event):
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        action = context_menu.exec(self.mapToGlobal(event.pos()))
        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, "edge"):
            selected = item.edge
        if selected and action == bezierAct:
            selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct:
            selected.edge_type = EDGE_TYPE_DIRECT

    def handleNewNodeContextMenu(self, event):
        print("CONTEXT : NEW")

    def getNodeClassFromData(self, data):
        if "op_code" not in data:
            return Node
        print(data)
        return get_class_from_opcode(data["op_code"])

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)

    def onDrop(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()
            event.setDropAction(Qt.MoveAction)
            event.accept()
            mouse_position = event.pos()
            scene_position = self.scene.getView().mapToScene(mouse_position)
            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                self.scene.history.storeHistory(
                    "Create node %s" % node.__class__.__name__
                )
            except Exception as e:
                dumpException(e)
        else:
            event.ignore()

    def sizeHint(self):
        return QSize(800, 600)

    def createStatusBar(self):
        """Create Status bar and connect to `Graphics View` scenePosChanged event"""
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        self.tabs_project.model_tab.nodeEditor.view.scenePosChanged.connect(
            self.onScenePosChanged
        )

    def createActions(self):
        """Create basic `File` and `Edit` actions"""
        self.actNew = QAction(
            "&New",
            self,
            shortcut="Ctrl+N",
            statusTip="Create new graph",
            triggered=self.onFileNew,
        )
        self.actOpen = QAction(
            "&Open",
            self,
            shortcut="Ctrl+O",
            statusTip="Open file",
            triggered=self.onFileOpen,
        )
        self.actSave = QAction(
            "&Save",
            self,
            shortcut="Ctrl+S",
            statusTip="Save file",
            triggered=self.onFileSave,
        )
        self.actSaveAs = QAction(
            "Save &As...",
            self,
            shortcut="Ctrl+Shift+S",
            statusTip="Save file as...",
            triggered=self.onFileSaveAs,
        )
        self.actSaveToCode = QAction(
            "&Save to code",
            self,
            shortcut="Ctrl+T",
            statusTip="Save node system to code",
            triggered=self.onFileSaveToCode,
        )
        self.actSaveAsToCode = QAction(
            "&Save to code &As...",
            self,
            shortcut="Ctrl+Y",
            statusTip="Save node system to code as...",
            triggered=self.onFileSaveToCodeAs,
        )
        self.actExit = QAction(
            "E&xit",
            self,
            shortcut="Ctrl+Q",
            statusTip="Exit application",
            triggered=self.close,
        )

        self.actUndo = QAction(
            "&Undo",
            self,
            shortcut="Ctrl+Z",
            statusTip="Undo last operation",
            triggered=self.onEditUndo,
        )
        self.actRedo = QAction(
            "&Redo",
            self,
            shortcut="Ctrl+Shift+Z",
            statusTip="Redo last operation",
            triggered=self.onEditRedo,
        )
        self.actCut = QAction(
            "Cu&t",
            self,
            shortcut="Ctrl+X",
            statusTip="Cut to clipboard",
            triggered=self.onEditCut,
        )
        self.actCopy = QAction(
            "&Copy",
            self,
            shortcut="Ctrl+C",
            statusTip="Copy to clipboard",
            triggered=self.onEditCopy,
        )
        self.actPaste = QAction(
            "&Paste",
            self,
            shortcut="Ctrl+V",
            statusTip="Paste from clipboard",
            triggered=self.onEditPaste,
        )
        self.actDelete = QAction(
            "&Delete",
            self,
            shortcut="Del",
            statusTip="Delete selected items",
            triggered=self.onEditDelete,
        )

    def createMenus(self):
        """Create Menus for `File` and `Edit`"""
        self.createFileMenu()
        self.createEditMenu()

    def createFileMenu(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu("&File")
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actOpen)
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actSaveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actSaveToCode)
        self.fileMenu.addAction(self.actSaveAsToCode)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actExit)

    def createEditMenu(self):
        menubar = self.menuBar()
        self.editMenu = menubar.addMenu("&Edit")
        self.editMenu.addAction(self.actUndo)
        self.editMenu.addAction(self.actRedo)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actCut)
        self.editMenu.addAction(self.actCopy)
        self.editMenu.addAction(self.actPaste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.actDelete)

    def setTitle(self):
        """Function responsible for setting window title"""
        title = "Node Editor - "
        title += self.getCurrentNodeEditorWidget().getUserFriendlyFilename()

        self.setWindowTitle(title)

    def closeEvent(self, event):
        """Handle close event. Ask before we loose work"""
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def isModified(self) -> bool:
        """Has current :class:`~nodeeditor.node_scene.Scene` been modified?

        :return: ``True`` if current :class:`~nodeeditor.node_scene.Scene` has been modified
        :rtype: ``bool``
        """
        return self.getCurrentNodeEditorWidget().scene.isModified()

    def getCurrentNodeEditorWidget(self) -> NodeEditorWidget:
        """get current :class:`~nodeeditor.node_editor_widget`

        :return: get current :class:`~nodeeditor.node_editor_widget`
        :rtype: :class:`~nodeeditor.node_editor_widget`
        """
        return self.centralWidget().model_tab.nodeEditor

    def maybeSave(self) -> bool:
        """If current `Scene` is modified, ask a dialog to save the changes. Used before
        closing window / mdi child document

        :return: ``True`` if we can continue in the `Close Event` and shutdown. ``False`` if we should cancel
        :rtype: ``bool``
        """
        if not self.isModified():
            return True

        res = QMessageBox.warning(
            self,
            "About to loose your work?",
            "The document has been modified.\n Do you want to save your changes?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
        )

        if res == QMessageBox.Save:
            return self.onFileSave()
        elif res == QMessageBox.Cancel:
            return False

        return True

    def onScenePosChanged(self, x: int, y: int):
        """Handle event when cursor position changed on the `Scene`

        :param x: new cursor x position
        :type x:
        :param y: new cursor y position
        :type y:
        """
        self.status_mouse_pos.setText("Scene Pos: [%d, %d]" % (x, y))

    def getFileDialogDirectory(self):
        """Returns starting directory for ``QFileDialog`` file open/save"""
        return ""

    def getFileDialogFilter(self):
        """Returns ``str`` standard file open/save filter for ``QFileDialog``"""
        return "Graph (*.json);;All files (*)"

    def getCodeFileDialogFilter(self):
        """Returns ``str`` standard file open/save filter for ``QFileDialog``"""
        return "Python File (*.py);;C++ File (*.cpp) -- NOT IMPLEMENTED;;All files (*)"

    def onFileNew(self):
        """Hande File New operation"""
        if self.maybeSave():
            self.getCurrentNodeEditorWidget().fileNew()
            self.setTitle()

    def onFileOpen(self):
        """Handle File Open operation"""
        if self.maybeSave():
            fname, filter = QFileDialog.getOpenFileName(
                self,
                "Open graph from file",
                self.getFileDialogDirectory(),
                self.getFileDialogFilter(),
            )
            if fname != "" and os.path.isfile(fname):
                self.getCurrentNodeEditorWidget().fileLoad(fname)
                self.setTitle()

    def onFileSave(self):
        """Handle File Save operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.isFilenameSet():
                return self.onFileSaveAs()

            current_nodeeditor.fileSave()
            self.statusBar().showMessage(
                "Successfully saved %s" % current_nodeeditor.filename, 5000
            )

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"):
                current_nodeeditor.setTitle()
            else:
                self.setTitle()
            return True

    def onFileSaveAs(self):
        """Handle File Save As operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(
                self,
                "Save graph to file",
                self.getFileDialogDirectory(),
                self.getFileDialogFilter(),
            )
            if fname == "":
                return False

            current_nodeeditor.fileSave(fname)
            self.statusBar().showMessage(
                "Successfully saved as %s" % current_nodeeditor.filename, 5000
            )

            # support for MDI app
            if hasattr(current_nodeeditor, "setTitle"):
                current_nodeeditor.setTitle()
            else:
                self.setTitle()
            return True

    def onFileSaveToCode(self):
        """Handle File Save to Code operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            if not current_nodeeditor.isCodeFilenameSet():
                return self.onFileSaveToCodeAs()

            current_nodeeditor.fileSaveToCode()
            self.statusBar().showMessage(
                "Successfully saved %s" % current_nodeeditor.filename, 5000
            )

    def onFileSaveToCodeAs(self):
        """Handle File Save to Code As operation"""
        current_nodeeditor = self.getCurrentNodeEditorWidget()
        if current_nodeeditor is not None:
            fname, filter = QFileDialog.getSaveFileName(
                self,
                "Save graph to code file",
                self.getFileDialogDirectory(),
                self.getCodeFileDialogFilter(),
            )
            if fname == "":
                return False

            current_nodeeditor.fileSaveToCode(fname)
            self.statusBar().showMessage(
                "Successfully saved as %s" % current_nodeeditor.filename, 5000
            )

            return True

    def onEditUndo(self):
        """Handle Edit Undo operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.undo()

    def onEditRedo(self):
        """Handle Edit Redo operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.history.redo()

    def onEditDelete(self):
        """Handle Delete Selected operation"""
        if self.getCurrentNodeEditorWidget():
            self.getCurrentNodeEditorWidget().scene.getView().deleteSelected()

    def onEditCut(self):
        """Handle Edit Cut to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(
                delete=True
            )
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditCopy(self):
        """Handle Edit Copy to clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            data = self.getCurrentNodeEditorWidget().scene.clipboard.serializeSelected(
                delete=False
            )
            str_data = json.dumps(data, indent=4)
            QApplication.instance().clipboard().setText(str_data)

    def onEditPaste(self):
        """Handle Edit Paste from clipboard operation"""
        if self.getCurrentNodeEditorWidget():
            raw_data = QApplication.instance().clipboard().text()

            try:
                data = json.loads(raw_data)
            except ValueError as e:
                print("Pasting of not valid json data!", e)
                return

            # check if the json data are correct
            if "nodes" not in data:
                print("JSON does not contain any nodes!")
                return
            try:
                return self.getCurrentNodeEditorWidget().scene.clipboard.deserializeFromClipboard(
                    data
                )
            except:
                return

    def readSettings(self):
        """Read the permanent profile settings for this app"""
        settings = QSettings(self.name_company, self.name_product)
        pos = settings.value("pos", QPoint(200, 200))
        size = settings.value("size", QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        """Write the permanent profile settings for this app"""
        settings = QSettings(self.name_company, self.name_product)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
