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
    OP_NODE_EMBEDDING
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)


class CustomEmbeddingGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 105
        self.width = 200


class CustomEmbeddingContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Class Cardinality :", self)
        self.HL.addWidget(self.label)
        self.cardinal = QSpinBox(self)
        self.cardinal.setMinimum(1)
        self.cardinal.setMaximum(2147483647)
        self.cardinal.setAlignment(Qt.AlignRight)
        self.HL.addWidget(self.cardinal)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Output dim :", self)
        self.HL2.addWidget(self.label2)
        self.outputdim = QSpinBox(self)
        self.outputdim.setMinimum(1)
        self.outputdim.setMaximum(2147483647)
        self.outputdim.setSingleStep(1)
        self.outputdim.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.outputdim)

        self.VL.addLayout(self.HL2)


@register_node(OP_NODE_EMBEDDING)
class CustomNode_Embedding(CustomNode):
    icon = ""
    op_code = OP_NODE_EMBEDDING
    op_title = "Embedding"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        INodes = self.getInputs()
        input_length = ""
        if INodes:
            if INodes[0].shape is not None:
                if ([el for el in INodes[0].shape if el is not None] == INodes[0].shape).all():
                    input_length = (
                        ', input_length=['
                        + ", ".join([str(e) for e in INodes[0].shape])
                        + ']'
                    )
        self.tfrepr = (
            "keras.layers.Embedding(input_dim="
            + str(self.content.cardinal.value() + 1)
            + ", output_dim="
            + str(self.content.outputdim.value())
            + input_length
            + ')'
        )

    def initInnerClasses(self):
        self.content = CustomEmbeddingContent(self)
        self.grNode = CustomEmbeddingGraphic(self)
        self.content.outputdim.valueChanged.connect(self.evalImplementation)


    def EvalImpl_(self):
        INodes = self.getInputs()

        if INodes[0].type != "input":
            self.addError("Enbedding layer must follow an Input Layer")
            self.shape = None
            return

        self.shape = np.zeros(len(INodes[0].shape)+1)
        for i, v in enumerate(INodes[0].shape):
            self.shape[i] = v
        self.shape[-1] = self.content.outputdim.value()