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
    OP_NODE_DENSE
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomDenseGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 105
        self.width = 170


class CustomDenseContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Units :", self)
        self.HL.addWidget(self.label)
        self.units = QSpinBox(self)
        self.units.setMinimum(1)
        self.units.setMaximum(2147483647)
        self.units.setAlignment(Qt.AlignRight)
        self.units.setObjectName(self.node.content_label_objname)
        self.HL.addWidget(self.units)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Use bias ? :", self)
        self.HL2.addWidget(self.label2)
        self.usebias = QCheckBox(self)
        self.usebias.setChecked(True)
        self.HL2.addWidget(self.usebias)

        self.VL.addLayout(self.HL2)

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


@register_node(OP_NODE_DENSE)
class CustomNode_Dense(CustomNode):
    icon = ""
    op_code = OP_NODE_DENSE
    op_title = "Dense"
    content_label = ""
    content_label_objname = "custom_node_dense"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.nononeinputshape = True

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.Dense(units="
            + str(self.content.units.value())
            + ", use_bias="
            + ("True" if self.content.usebias.isChecked() else "False")
            + ', activation="'
            + self.content.activation.currentText()
            + '"'
            + ")"
        )

    def initInnerClasses(self):
        self.content = CustomDenseContent(self)
        self.grNode = CustomDenseGraphic(self)
        self.content.units.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()
        self.shape = np.array(INodes[0].shape)
        self.shape[-1] = self.content.units.value()
