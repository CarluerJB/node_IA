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
    OP_NODE_UPSAMPLING3D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomUpSampling3DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 355


class CustomUpSampling3DContent(QDMNodeContentWidget):
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
        self.kernelsizez = QSpinBox(self)
        self.kernelsizez.setMinimum(1)
        self.kernelsizez.setMaximum(2147483647)
        self.kernelsizez.setSingleStep(1)
        self.kernelsizez.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizez)
        self.VL.addLayout(self.HL2)


@register_node(OP_NODE_UPSAMPLING3D)
class CustomNode_UpSampling2D(CustomNode):
    icon = ""
    op_code = OP_NODE_UPSAMPLING3D
    op_title = "UpSampling3D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.UpSampling3D(size=("
            + str(self.content.kernelsizex.value())
            + ", "
            + str(self.content.kernelsizey.value())
            + ", "
            + str(self.content.kernelsizez.value())
            + "))"
        )

    def initInnerClasses(self):
        self.content = CustomUpSampling3DContent(self)
        self.grNode = CustomUpSampling3DGraphic(self)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizez.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if not self.content.kernelsizex.value() == self.content.kernelsizey.value() == self.content.kernelsizez.value():
            self.addWarning(
                "Kernel size of different values", self.content.label2, "color: red;"
            )

        INodes = self.getInputs()

        if len(INodes[0].shape) != 4:
            self.addError("MaxPooling3D need input shape of exactly size 4")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[0] *= self.content.kernelsizex.value()
        self.shape[1] *= self.content.kernelsizey.value()
        self.shape[2] *= self.content.kernelsizez.value()

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
