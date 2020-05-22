from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox
)

from PyQt5.QtCore import Qt

import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_SIMPLE_CONV
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomSimpleConvGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 140
        self.width = 165


class CustomSimpleConvContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Filters :", self)
        self.HL.addWidget(self.label)
        self.filters = QSpinBox(self)
        self.filters.setMinimum(1)
        self.filters.setMaximum(2147483647)
        self.filters.setAlignment(Qt.AlignRight)
        self.HL.addWidget(self.filters)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Kernel Size :", self)
        self.HL2.addWidget(self.label2)
        self.kernelsize = QSpinBox(self)
        self.kernelsize.setMinimum(1)
        self.kernelsize.setMaximum(2147483647)
        self.kernelsize.setSingleStep(2)
        self.kernelsize.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsize)

        self.VL.addLayout(self.HL2)

        self.HL5 = QHBoxLayout(self)
        self.label5 = QLabel("Activation :", self)
        self.HL5.addWidget(self.label5)
        self.activation = QComboBox(self)
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        self.activation.addItem("relu")
        self.activation.addItem("sigmoid")
        self.HL5.addWidget(self.activation)

        self.VL.addLayout(self.HL5)


@register_node(OP_NODE_SIMPLE_CONV)
class CustomNode_SimpleConv(CustomNode):
    icon = ""
    op_code = OP_NODE_SIMPLE_CONV
    op_title = "Convolution (simple)"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        INODES = self.getInputs()
        ND = "1"
        if INODES:
            if INODES[0]:
                ND = str(len(INODES[0].shape) - 1)

        self.tfrepr = (
            "keras.layers.Conv" + ND +  "D(filters="
            + str(self.content.filters.value())
            + ", kernel_size="
            + str(self.content.kernelsize.value())
            + ', padding="same"'
            + ', activation="'
            + self.content.activation.currentText()
            + '"'
            + ")"
        )

    def initInnerClasses(self):
        self.content = CustomSimpleConvContent(self)
        self.grNode = CustomSimpleConvGraphic(self)
        self.content.filters.valueChanged.connect(self.evalImplementation)
        self.content.kernelsize.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) > 4 or len(INodes[0].shape) < 2:
            self.addError("Convolution need vectors/images/3D as input shape")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[-1] = self.content.filters.value()
