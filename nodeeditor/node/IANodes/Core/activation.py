from PyQt5.QtWidgets import (
    QVBoxLayout,
    QComboBox
)

from PyQt5.QtCore import Qt

import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_ACTIVATION
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)

class CustomActivationContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.activation = QComboBox(self)
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("relu")
        self.activation.addItem("tanh")
        self.activation.addItem("sigmoid")
        self.activation.addItem("hard_sigmoid")
        self.activation.addItem("exponential")
        # self.comboBox.addItem("elu")
        # self.comboBox.addItem("selu")
        # # self.comboBox.addItem("LeakyReLu")
        # self.comboBox.addItem("PReLu")
        # self.comboBox.addItem("ThresholdedReLU")
        self.setLayout(self.layout)
        self.layout.addWidget(self.activation, Qt.AlignLeft)


@register_node(OP_NODE_ACTIVATION)
class CustomNode_Activation(CustomNode):
    icon = ""
    op_code = OP_NODE_ACTIVATION
    op_title = "Activation"
    content_label = ""
    content_label_objname = "custom_node_activation"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            'keras.layers.Activation("' + self.content.activation.currentText() + '")'
        )

    def initInnerClasses(self):
        self.content = CustomActivationContent(self)
        self.grNode = CustomGraphicsNode(self)
