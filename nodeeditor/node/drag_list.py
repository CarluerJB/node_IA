import json
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QListView, QListWidgetItem
from PyQt5.QtGui import QPixmap, QIcon, QDrag
from PyQt5.QtCore import (
    QSize,
    Qt,
    QByteArray,
    QDataStream,
    QIODevice,
    QMimeData,
    QPoint,
)

from nodeeditor.node.content_conf import (
    CUSTOM_NODES,
    get_class_from_opcode,
    LISTBOX_MIMETYPE,
)


class NodeDragList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setIconSize(QSize(600, 600))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setFlow(QListView.LeftToRight)
        self.addMyItems()

    def addMyItems(self):
        keys = list(CUSTOM_NODES.keys())
        keys.sort()
        for key in keys:
            node = get_class_from_opcode(key)
            self.addMyItem(node.op_title, node.icon, node.op_code)

    def addMyItem(self, name, icon=None, op_code=0):
        item = QListWidgetItem(name, self)
        pixmap = QPixmap(icon if icon is not None else ".")
        item.setIcon(QIcon(pixmap))
        item.setSizeHint(QSize(200, 50))
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

        item.setData(Qt.UserRole, pixmap)
        item.setData(Qt.UserRole + 1, op_code)

    def startDrag(self, supportedActions):
        try:
            item = self.currentItem()
            op_code = item.data(Qt.UserRole + 1)
            pixmap = QPixmap(item.data(Qt.UserRole))
            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text())
            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)
            drag.exec(Qt.MoveAction)
        except Exception:
            pass
