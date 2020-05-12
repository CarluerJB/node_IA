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
    OP_NODE_MAXPOOLING2D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomMaxPooling2DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 255


class CustomMaxPooling2DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Pool Size :", self)
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
        self.use_strides = QCheckBox(self)
        self.HL3.addWidget(self.use_strides)
        self.use_strides.setChecked(False)
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


@register_node(OP_NODE_MAXPOOLING2D)
class CustomNode_MaxPooling2D(CustomNode):
    icon = ""
    op_code = OP_NODE_MAXPOOLING2D
    op_title = "MaxPooling2D"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.MaxPooling2D(pool_size=("
            + str(self.content.kernelsizex.value())
            + ", "
            + str(self.content.kernelsizey.value())
            + ")"
            + ", strides="
            + (('(' +  str(self.content.stridesx.value())
            + ", "
            + str(self.content.stridesy.value())
            + ")") if self.content.use_strides.isChecked() else "None")
            + ', padding="'
            + self.content.padding.currentText()
            + '")'
        )

    def initInnerClasses(self):
        self.content = CustomMaxPooling2DContent(self)
        self.grNode = CustomMaxPooling2DGraphic(self)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)
        self.content.stridesx.valueChanged.connect(self.evalImplementation)
        self.content.stridesy.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)
        self.content.use_strides.stateChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
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
            self.addError("MaxPooling2D need input shape of exactly size 3")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        if self.shape[0] is not None:
            self.shape[0] -= (
                (self.content.kernelsizex.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )

            value = self.content.kernelsizex.value()
            if self.content.use_strides.isChecked():
                value = self.content.stridesx.value()

            self.shape[0] = (self.shape[0] // value) + (
                1 if self.shape[0] % value != 0 else 0
            )
        else:
            self.shape[0] = None

        if self.shape[1] is not None:
            self.shape[1] -= (
                (self.content.kernelsizey.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )

            value = self.content.kernelsizey.value()
            if self.content.use_strides.isChecked():
                value = self.content.stridesy.value()

            self.shape[1] = (self.shape[1] // value) + (
                1 if self.shape[1] % value != 0 else 0
            )
        else:
            self.shape[1] = None

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
        self.content.label3.setStyleSheet("color : white;")
