from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRectF
from nodeeditor.node.node import Node
from nodeeditor.node.content_widget import QDMNodeContentWidget
from nodeeditor.node.graphics_node import QDMGraphicsNode
from nodeeditor.node.socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException
import numpy as np


class CustomGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("nodeeditor/images/status_icons.png")

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty():
            offset = 0.0
        if self.node.isInvalid():
            offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0), self.icons, QRectF(offset, 0, 24.0, 24.0)
        )


class CustomContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class CustomNode(Node):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    def __init__(self, scene, inputs=[2, 2], outputs=[2, 2]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.value = None
        self.shape = None
        self.grNodeToolTip = ""
        self.nononeinputshape = False
        self.setType()
        self.updatetfrepr()
        self.evalImplementation()

    def setType(self):
        print("----")
        self.type = "hidden"
        print(self.type)

    def updatetfrepr(self):
        self.tfrepr = "pass"

    def addInfo(self, message: str, which=None, stylesheet=None):
        self.grNodeToolTip += "INFO : " + message + "\n"
        if which is not None:
            which.setToolTip("INFO : " + message)
            if stylesheet is not None:
                which.setStyleSheet(stylesheet)

    def addWarning(self, message: str, which=None, stylesheet=None):
        self.markDirty(True)
        self.grNodeToolTip += "WARNING : " + message + "\n"
        if which is not None:
            which.setToolTip("WARNING : " + message)
            if stylesheet is not None:
                which.setStyleSheet(stylesheet)

    def addError(self, message: str, which=None, stylesheet=None):
        self.markInvalid(True)
        self.grNodeToolTip += "ERROR : " + message + "\n"
        if which is not None:
            which.setToolTip("ERROR : " + message)
            if stylesheet is not None:
                which.setStyleSheet(stylesheet)

    def initSettings(self):
        super().initSettings()
        self.output_multi_edged = True

    def initInnerClasses(self):
        self.content = CustomContent(self)
        self.grNode = CustomGraphicsNode(self)

    def codealize(self):
        res = super().codealize()
        # update representation
        self.updatetfrepr()
        res["op_code"] = self.__class__.op_code
        res["tfrepr"] = self.tfrepr
        res["type"] = self.type
        return res

    def serialize(self):
        res = super().serialize()
        res["op_code"] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res

    def evalOperation(self, array):
        return 0

    def EvalImpl_(self):
        """
        Default behavior is : return the same shape as the input one
        """
        if self.type != "input":
            INodes = self.getInputs()
            self.shape = np.array(INodes[0].shape)

    def endEval(self):
        if self.shape is not None and len(self.shape) == 1:
            self.shape = np.array(self.shape)
        self.grNode.setToolTip(self.grNodeToolTip)
        if self.type != "output":
            self.outputs[0].grSocket.setToolTip(str(self.shape))
            for nn in self.getOutputs():
                nn.evalImplementation()

    def resetAll(self):
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")
        self.grNodeToolTip = ""
        self.shape = None

    def evalImplementation(self):
        self.resetAll()

        if self.type != "input":
            if len(self.getInputs()) == 0:
                self.addError("Layer with no Inputs")
                self.shape = None
                self.endEval()
                return

            for node in self.getInputs():
                if node.shape is None:
                    self.addError("Bad input shape")
                    self.shape = None
                    self.endEval()
                    return

            for node in self.getInputs():
                for val in node.shape:
                    if val is None:
                        if self.nononeinputshape:
                            self.addError("This layer does not support None Input Shape")
                            self.shape = None
                            self.endEval()
                            return
                        self.addInfo("Input shape contains None value")
                        break

        self.EvalImpl_()

        self.endEval()

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(
                " _> returning cached %s value:" % self.__class__.__name__, self.value
            )
            return self.value
        try:
            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()
