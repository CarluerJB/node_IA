from PyQt5.QtCore import Qt

import numpy as np

import ast

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QLineEdit
)

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_SIMPLE_INPUT_VALUE
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)

from nodeeditor.node.socket import (
    LEFT_TOP,
    RIGHT_TOP,
)

class CustomSimpleInputValueContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.ishape = QLineEdit("[32, 32, 3]", self)
        self.HL.addWidget(self.ishape)
        self.ishape.setAlignment(Qt.AlignRight)
        self.ishape.setObjectName(self.node.content_label_objname)

        self.VL.addLayout(self.HL)

@register_node(OP_NODE_SIMPLE_INPUT_VALUE)
class CustomNode_Input(CustomNode):
    icon = ""
    op_code = OP_NODE_SIMPLE_INPUT_VALUE
    op_title = "Input Value (simple)"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])

    def setType(self):
        self.type = "input"

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Input(" + self.content.ishape.text() + ")"

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True
        self.input_can_be_added = False
        self.output_can_be_added = False

    def initInnerClasses(self):
        self.content = CustomSimpleInputValueContent(self)
        self.grNode = CustomGraphicsNode(self)
        self.content.ishape.textChanged.connect(self.onInputChanged)

    def EvalImpl_(self):
        try:
            s_value = ast.literal_eval(self.content.ishape.text())
            self.shape = np.array(s_value)
        except Exception:
            self.shape = None
            self.addError("Invalid shape")
