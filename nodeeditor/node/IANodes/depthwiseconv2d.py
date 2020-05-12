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
    OP_NODE_DWCONV2D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomDWConv2DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 255


class CustomDWConv2DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Depth Multiplier :", self)
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

        self.HL3 = QHBoxLayout(self)
        self.label3 = QLabel("Strides :", self)
        self.HL3.addWidget(self.label3)
        self.stridesx = QSpinBox(self)
        self.stridesx.setMinimum(1)
        self.stridesx.setMaximum(2147483647)
        self.stridesx.setSingleStep(1)
        self.stridesx.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.stridesx)
        self.stridesy = QSpinBox(self)
        self.stridesy.setMinimum(1)
        self.stridesy.setMaximum(2147483647)
        self.stridesy.setSingleStep(1)
        self.stridesy.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.stridesy)

        self.VL.addLayout(self.HL3)

        self.HL4 = QHBoxLayout(self)
        self.label4 = QLabel("Padding :", self)
        self.HL4.addWidget(self.label4)
        self.padding = QComboBox(self)
        self.padding.addItem("valid")
        self.padding.addItem("same")
        self.HL4.addWidget(self.padding)

        self.VL.addLayout(self.HL4)

        self.HL5 = QHBoxLayout(self)
        self.label5 = QLabel("Activation :", self)
        self.HL5.addWidget(self.label5)
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
        self.HL5.addWidget(self.activation)

        self.VL.addLayout(self.HL5)


@register_node(OP_NODE_DWCONV2D)
class CustomNode_DepthWiseConv2D(CustomNode):
    icon = ""
    op_code = OP_NODE_DWCONV2D
    op_title = "DepthwiseConv2D"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.DepthwiseConv2D(depth_multiplier="
            + str(self.content.filters.value())
            + ", kernel_size=("
            + str(self.content.kernelsizex.value())
            + ", "
            + str(self.content.kernelsizey.value())
            + ")"
            + ", strides=("
            + str(self.content.stridesx.value())
            + ", "
            + str(self.content.stridesy.value())
            + ")"
            + ', padding="'
            + self.content.padding.currentText()
            + '"'
            + ', activation="'
            + self.content.activation.currentText()
            + '"'
            + ")"
        )

    def initInnerClasses(self):
        self.content = CustomDWConv2DContent(self)
        self.grNode = CustomDWConv2DGraphic(self)
        self.content.filters.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)
        self.content.stridesx.valueChanged.connect(self.evalImplementation)
        self.content.stridesy.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if self.content.kernelsizex.value() % 2 == 0:
            self.addWarning(
                "Even kernel size at pos 1",
                self.content.kernelsizex,
                "background-color: yellow;",
            )

        if self.content.kernelsizey.value() % 2 == 0:
            self.addWarning(
                "Even kernel size at pos 2",
                self.content.kernelsizey,
                "background-color: yellow;",
            )

        if self.content.kernelsizex.value() != self.content.kernelsizey.value():
            self.addWarning(
                "Kernel size of different values", self.content.label2, "color: red;"
            )

        if self.content.stridesx.value() != self.content.stridesy.value():
            self.addWarning(
                "Strides of different values", self.content.label3, "color: red;"
            )

        INodes = self.getInputs()

        if len(INodes[0].shape) != 3:
            self.addError("Conv2D need input shape of exactly size 3")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[2] *= self.content.filters.value()

        if self.shape[0] is not None:
            self.shape[0] -= (
                (self.content.kernelsizex.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )
            self.shape[0] = (self.shape[0] // self.content.stridesx.value()) + (
                1 if self.shape[0] % self.content.stridesx.value() != 0 else 0
            )
        else:
            self.shape[0] = None

        if self.shape[1] is not None:
            self.shape[1] -= (
                (self.content.kernelsizey.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )
            self.shape[1] = (self.shape[1] // self.content.stridesy.value()) + (
                1 if self.shape[1] % self.content.stridesy.value() != 0 else 0
            )
        else:
            self.shape[1] = None

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
        self.content.label3.setStyleSheet("color : white;")

        self.content.kernelsizex.setStyleSheet("background-color: white;")
        self.content.kernelsizex.setToolTip("")
        self.content.kernelsizey.setStyleSheet("background-color: white;")
        self.content.kernelsizey.setToolTip("")
