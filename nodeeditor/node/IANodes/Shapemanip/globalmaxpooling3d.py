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
    OP_NODE_GLOBALMAXPOOLING3D
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    QDMNodeContentWidget,
    CustomNode
)

@register_node(OP_NODE_GLOBALMAXPOOLING3D)
class CustomNode_GlobalMaxPooling3D(CustomNode):
    icon = ""
    op_code = OP_NODE_GLOBALMAXPOOLING3D
    op_title = "GlobalMaxPooling3D"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = (
            "keras.layers.GlobalMaxPooling3D()"
        )

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 4:
            self.addError("GlobalMaxPooling3D need input shape of exactly size 4")
            self.shape = None
            return

        self.shape = [0]
        self.shape[0] = np.array(INodes[0].shape[3])
