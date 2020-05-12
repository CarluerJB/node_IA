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
    OP_NODE_UPSAMPLING1D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomUpSampling1DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 170


class CustomUpSampling1DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Size :", self)
        self.HL2.addWidget(self.label2)
        self.size = QSpinBox(self)
        self.size.setMinimum(1)
        self.size.setMaximum(2147483647)
        self.size.setSingleStep(1)
        self.size.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.size)

        self.VL.addLayout(self.HL2)

@register_node(OP_NODE_UPSAMPLING1D)
class CustomNode_UpSampling1D(CustomNode):
    icon = ""
    op_code = OP_NODE_UPSAMPLING1D
    op_title = "UpSampling1D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.UpSampling1D(size="
            + str(self.content.kernelsize.value())
            + ')'
        )

    def initInnerClasses(self):
        self.content = CustomUpSampling1DContent(self)
        self.grNode = CustomUpSampling1DGraphic(self)
        self.content.size.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 2:
            self.addError("UpSampling1D need input shape of exactly size 2")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)
        self.shape[0] *= self.content.size.value()
