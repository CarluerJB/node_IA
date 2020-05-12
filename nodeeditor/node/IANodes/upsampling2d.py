from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QComboBox,
    QCheckBox
)

from PyQt5.QtCore import Qt

import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_UPSAMPLING2D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomUpSampling2DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 255


class CustomUpSampling2DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Size :", self)
        self.HL2.addWidget(self.label2)
        self.kernelsizex = QSpinBox(self)
        self.kernelsizex.setMinimum(1)
        self.kernelsizex.setMaximum(2147483647)
        self.kernelsizex.setSingleStep(1)
        self.kernelsizex.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizex)
        self.kernelsizey = QSpinBox(self)
        self.kernelsizey.setMinimum(1)
        self.kernelsizey.setMaximum(2147483647)
        self.kernelsizey.setSingleStep(1)
        self.kernelsizey.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizey)

        self.VL.addLayout(self.HL2)


@register_node(OP_NODE_UPSAMPLING2D)
class CustomNode_UpSampling2D(CustomNode):
    icon = ""
    op_code = OP_NODE_UPSAMPLING2D
    op_title = "UpSampling2D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.UpSampling2D(size=("
            + str(self.content.kernelsizex.value())
            + ", "
            + str(self.content.kernelsizey.value())
            + "))"
        )

    def initInnerClasses(self):
        self.content = CustomUpSampling2DContent(self)
        self.grNode = CustomUpSampling2DGraphic(self)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if self.content.kernelsizex.value() != self.content.kernelsizey.value():
            self.addWarning(
                "Kernel size of different values", self.content.label2, "color: red;"
            )

        INodes = self.getInputs()

        if len(INodes[0].shape) != 3:
            self.addError("MaxPooling2D need input shape of exactly size 3")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[0] *= self.content.kernelsizex.value()
        self.shape[1] *= self.content.kernelsizey.value()

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
