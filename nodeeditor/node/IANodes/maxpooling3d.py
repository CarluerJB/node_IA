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
    OP_NODE_MAXPOOLING3D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomMaxPooling3DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 355


class CustomMaxPooling3DContent(QDMNodeContentWidget):
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
        self.kernelsizez = QSpinBox(self)
        self.kernelsizez.setMinimum(1)
        self.kernelsizez.setMaximum(2147483647)
        self.kernelsizez.setSingleStep(1)
        self.kernelsizez.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizez)

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
        self.stridesz = QSpinBox(self)
        self.stridesz.setMinimum(1)
        self.stridesz.setMaximum(2147483647)
        self.stridesz.setSingleStep(1)
        self.stridesz.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.stridesz)

        self.VL.addLayout(self.HL3)

        self.HL4 = QHBoxLayout(self)
        self.label4 = QLabel("Padding :", self)
        self.HL4.addWidget(self.label4)
        self.padding = QComboBox(self)
        self.padding.addItem("valid")
        self.padding.addItem("same")
        self.HL4.addWidget(self.padding)

        self.VL.addLayout(self.HL4)



@register_node(OP_NODE_MAXPOOLING3D)
class CustomNode_MaxPooling3D(CustomNode):
    icon = ""
    op_code = OP_NODE_MAXPOOLING3D
    op_title = "MaxPooling3D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.Conv3D(pool_size=("
            + str(self.content.kernelsizex.value())
            + ", "
            + str(self.content.kernelsizey.value())
            + ", "
            + str(self.content.kernelsizez.value())
            + ")"
            + ", strides="
            + (('(' + str(self.content.stridesx.value())
            + ", "
            + str(self.content.stridesy.value())
            + ", "
            + str(self.content.stridesz.value())
            + ")") if self.content.use_strides.isChecked() else "None")
            + ', padding="'
            + self.content.padding.currentText()
            + '")'
        )

    def initInnerClasses(self):
        self.content = CustomMaxPooling3DContent(self)
        self.grNode = CustomMaxPooling3DGraphic(self)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizez.valueChanged.connect(self.evalImplementation)
        self.content.stridesx.valueChanged.connect(self.evalImplementation)
        self.content.stridesy.valueChanged.connect(self.evalImplementation)
        self.content.stridesz.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)
        self.content.use_strides.stateChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if not self.content.kernelsizex.value() == self.content.kernelsizey.value() == self.content.kernelsizez.value():
            self.addWarning(
                "Kernel size of different values", self.content.label2, "color: red;"
            )

        if not self.content.stridesx.value() == self.content.stridesy.value() == self.content.stridesz.value():
            self.addWarning(
                "Strides of different values", self.content.label3, "color: red;"
            )

        INodes = self.getInputs()

        if len(INodes[0].shape) != 4:
            self.addError("MaxPooling3D need input shape of exactly size 4")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        if self.shape[0] != None:
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

        if self.shape[1] != None:
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

        if self.shape[2] != None:
            self.shape[2] -= (
                (self.content.kernelsizez.value() - 1)
                if self.content.padding.currentText() == "valid"
                else 0
            )

            value = self.content.kernelsizez.value()
            if self.content.use_strides.isChecked():
                value = self.content.stridesz.value()

            self.shape[2] = (self.shape[2] // value) + (
                1 if self.shape[2] % value != 0 else 0
            )
        else:
            self.shape[2] = None

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
        self.content.label3.setStyleSheet("color : white;")
