import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_SQUEEZE
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    CustomNode
)

from nodeeditor.node.socket import (
    LEFT_TOP,
    RIGHT_TOP,
)

@register_node(OP_NODE_SQUEEZE)
class CustomNode_Squeeze(CustomNode):
    icon = ""
    op_code = OP_NODE_SQUEEZE
    op_title = "Squeeze"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        INodes = self.getInputs()
        if INodes:
            if INodes[0].shape is not None:
                idx = []
                for i, v in enumerate(INodes[0].shape):
                    if v == 1:
                        idx.append(str(i + 1))
                if idx:
                    self.tfrepr = (
                        "keras.layers.Lambda(lambda x: tf.squeeze(x, ["
                        + ", ".join(idx)
                        + "]))"
                    )
                    return
        self.tfrepr = (
            "keras.layers.Lambda(lambda x: x)"
        )


    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP

    def initInnerClasses(self):
        self.grNode = CustomGraphicsNode(self)

    def EvalImpl_(self):
        INodes = self.getInputs()

        self.shape = np.array([val for val in INodes[0].shape if val != 1])
