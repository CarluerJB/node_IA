import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_MAX
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    CustomNode
)

from nodeeditor.node.socket import (
    LEFT_TOP,
    RIGHT_TOP,
)

@register_node(OP_NODE_MAX)
class CustomNode_Max(CustomNode):
    icon = ""
    op_code = OP_NODE_MAX
    op_title = "Maximum"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Maximum()"

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = True

    def initInnerClasses(self):
        self.grNode = CustomGraphicsNode(self)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes) == 1:
            self.addWarning("Only one input connected")
            self.shape = np.array(INodes[0].shape)
            return

        firstshape = INodes[0].shape
        for node in INodes[1:]:
            if not (
                (len(node.shape) == len(firstshape))
                and (node.shape == firstshape).all()
            ):
                self.addError("Input shape mismatch")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)
