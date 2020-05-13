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
    OP_NODE_GLOBALMAXPOOLING1D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)

@register_node(OP_NODE_GLOBALMAXPOOLING1D)
class CustomNode_GlobalMaxPooling1D(CustomNode):
    icon = ""
    op_code = OP_NODE_GLOBALMAXPOOLING1D
    op_title = "GlobalMaxPooling1D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.GlobalMaxPooling1D()"
        )

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 2:
            self.addError("GlobalMaxPooling1D need input shape of exactly size 2")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape[1])
