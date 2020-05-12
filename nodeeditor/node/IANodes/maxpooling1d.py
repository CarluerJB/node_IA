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
    OP_NODE_MAXPOOLING1D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomMaxPooling1DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 170


class CustomMaxPooling1DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Pool Size :", self)
        self.HL2.addWidget(self.label2)
        self.kernelsize = QSpinBox(self)
        self.kernelsize.setMinimum(1)
        self.kernelsize.setMaximum(2147483647)
        self.kernelsize.setSingleStep(1)
        self.kernelsize.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsize)

        self.VL.addLayout(self.HL2)

        self.HL3 = QHBoxLayout(self)
        self.label3 = QLabel("Strides :", self)
        self.HL3.addWidget(self.label3)
        self.strides = QSpinBox(self)
        self.strides.setMinimum(1)
        self.strides.setMaximum(2147483647)
        self.strides.setSingleStep(1)
        self.strides.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.strides)

        self.VL.addLayout(self.HL3)

        self.HL4 = QHBoxLayout(self)
        self.label4 = QLabel("Padding :", self)
        self.HL4.addWidget(self.label4)
        self.padding = QComboBox(self)
        self.padding.addItem("valid")
        self.padding.addItem("same")
        self.HL4.addWidget(self.padding)

        self.VL.addLayout(self.HL4)


@register_node(OP_NODE_MAXPOOLING1D)
class CustomNode_MaxPooling1D(CustomNode):
    icon = ""
    op_code = OP_NODE_MAXPOOLING1D
    op_title = "MaxPooling1D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.MaxPooling1D(pool_size="
            + str(self.content.kernelsize.value())
            + ", strides="
            + str(self.content.strides.value())
            + ', padding="'
            + self.content.padding.currentText()
            + '")'
        )

    def initInnerClasses(self):
        self.content = CustomMaxPooling1DContent(self)
        self.grNode = CustomMaxPooling1DGraphic(self)
        self.content.kernelsize.valueChanged.connect(self.evalImplementation)
        self.content.strides.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 2:
            self.addError("MaxPooling1D need input shape of exactly size 2")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[0] -= (
            (self.content.kernelsize.value() - 1)
            if self.content.padding.currentText() == "valid"
            else 0
        )
        self.shape[0] = (self.shape[0] // self.content.strides.value()) + (
            1 if self.shape[0] % self.content.strides.value() != 0 else 0
        )
