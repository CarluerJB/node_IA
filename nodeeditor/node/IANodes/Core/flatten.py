import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_FLATTEN
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    CustomNode
)

from nodeeditor.node.socket import (
    LEFT_TOP,
    RIGHT_TOP,
)

@register_node(OP_NODE_FLATTEN)
class CustomNode_Add(CustomNode):
    icon = ""
    op_code = OP_NODE_FLATTEN
    op_title = "Flatten"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.nononeinputshape = True

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Flatten()"

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP

    def initInnerClasses(self):
        self.grNode = CustomGraphicsNode(self)

    def EvalImpl_(self):
        shape = np.array(self.getInputs()[0].shape)
        self.shape = [1]
        for val in shape:
            if val is not None:
                self.shape[0] *= val
            else:
                self.shape[0] = None
                break
