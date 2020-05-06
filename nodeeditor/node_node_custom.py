from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
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
        if self.node.isDirty(): offset=0.0
        if self.node.isInvalid(): offset=48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        
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
    def __init__(self, scene, inputs=[2,2], outputs=[2,2]):

        super().__init__(scene, self.__class__.op_title, inputs, outputs)
        self.value = None
        self.markDirty()

    
    def initInnerClasses(self):
        self.content = CustomContent(self)
        self.grNode = CustomGraphicsNode(self)
    
    
    def codealize(self):
        res = super().codealize()
        res['op_code'] = self.__class__.op_code
        return res
    
    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
    
    def evalImplementation(self):
        inputs = []
        inputs_eval=[]
        for i in range(0,len(self.inputs)):
            inputs.append(self.getInputs(i))
        
        
        if None in inputs:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None
        else:
            for i in range(0, len(inputs)):
                for edge in inputs[i]:
                    inputs_eval.append(edge.eval())
            val = self.evalOperation(np.array(inputs_eval))
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

    # def evalImplementation(self):
    #     i1 = self.getInput(0)
    #     i2 = self.getInput(1)

    #     if i1 is None or i2 is None:
    #         self.markInvalid()
    #         self.markDescendantsDirty()
    #         self.grNode.setToolTip("Connect all inputs")
    #         return None

    #     else:
    #         val = self.evalOperation(i1.eval(), i2.eval())
    #         self.value = val
    #         self.markDirty(False)
    #         self.markInvalid(False)
    #         self.grNode.setToolTip("")

    #         self.markDescendantsDirty()
    #         self.evalChildren()

    #         return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
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