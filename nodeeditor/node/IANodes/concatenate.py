
import numpy as np

from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_CONCAT
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    CustomNode
)

@register_node(OP_NODE_CONCAT)
class CustomNode_Concat(CustomNode):
    icon = ""
    op_code = OP_NODE_CONCAT
    op_title = "Concatenate"
    content_label = ""
    content_label_objname = "custom_node_concat"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Concatenate()"

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def initInnerClasses(self):
        # self.content = CustomDenseContent(self)
        self.grNode = CustomGraphicsNode(self)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes) == 1:
            self.addWarning("Only one input connected")
            self.shape = np.array(INodes[0].shape)
            return

        firstshape = INodes[0].shape
        for node in INodes[1:]:
            print(node)
            if (
                len(node.shape) != len(firstshape)
                or (node.shape[:-1] != firstshape[:-1]).any()
            ):
                self.addError("Input shape mismatch")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)
        for node in INodes[1:]:
            self.shape[-1] += node.shape[-1]
