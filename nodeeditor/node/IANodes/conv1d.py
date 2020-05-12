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
    OP_NODE_CONV1D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomConv1DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 170


class CustomConv1DContent(QDMNodeContentWidget):
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


@register_node(OP_NODE_CONV1D)
class CustomNode_Conv1D(CustomNode):
    icon = ""
    op_code = OP_NODE_CONV1D
    op_title = "Conv1D"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.Conv1D(filters="
            + str(self.content.filters.value())
            + ", kernel_size="
            + str(self.content.kernelsize.value())
            + ", strides="
            + str(self.content.strides.value())
            + ', padding="'
            + self.content.padding.currentText()
            + '", activation="'
            + self.content.activation.currentText()
            + '")'
        )

    def initInnerClasses(self):
        self.content = CustomConv1DContent(self)
        self.grNode = CustomConv1DGraphic(self)
        self.content.filters.valueChanged.connect(self.evalImplementation)
        self.content.kernelsize.valueChanged.connect(self.evalImplementation)
        self.content.strides.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if self.content.kernelsize.value() % 2 == 0:
            self.addWarning(
                "Even kernel size",
                self.content.kernelsize,
                "background-color: yellow;",
            )

        INodes = self.getInputs()

        if len(INodes[0].shape) != 2:
            self.addError("Conv1D need input shape of exactly size 2")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[1] = self.content.filters.value()

        if self.shape[0] is not None:
            self.shape[0] -= (
                (self.content.kernelsize.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )
            self.shape[0] = (self.shape[0] // self.content.strides.value()) + (
                1 if self.shape[0] % self.content.strides.value() != 0 else 0
            )
        else:
            self.shape[0] = None

    def resetAll(self):
        super().resetAll()
        self.content.kernelsize.setStyleSheet("background-color: white;")
        self.content.kernelsize.setToolTip("")
