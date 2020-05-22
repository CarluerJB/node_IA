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
    OP_NODE_GLOBALMAXPOOLING2D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)

@register_node(OP_NODE_GLOBALMAXPOOLING2D)
class CustomNode_GlobalMaxPooling2D(CustomNode):
    icon = ""
    op_code = OP_NODE_GLOBALMAXPOOLING2D
    op_title = "GlobalMaxPooling2D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.GlobalMaxPooling2D()"
        )

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 3:
            self.addError("GlobalMaxPooling2D need input shape of exactly size 3")
            self.shape = None
            return

        self.shape = [np.array(INodes[0].shape[2])]
