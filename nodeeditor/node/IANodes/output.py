from nodeeditor.node.content_conf import (
    register_node,
    OP_NODE_OUTPUT
)

from nodeeditor.node.node_custom import (
    CustomGraphicsNode,
    CustomNode
)

from nodeeditor.node.IANodes.activation import CustomActivationContent

@register_node(OP_NODE_OUTPUT)
class CustomNode_Output(CustomNode):
    icon = "nodeeditor/images/output.png"
    op_code = OP_NODE_OUTPUT
    op_title = "Output"
    content_label = "Out"
    content_label_objname = "custom_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])
        self.scene.addOutputs(self)

    def setType(self):
        self.type = "output"

    def updatetfrepr(self):
        self.tfrepr = (
            'keras.layers.Activation("' + self.content.activation.currentText() + '")'
        )

    def initInnerClasses(self):
        self.content = CustomActivationContent(self)
        self.grNode = CustomGraphicsNode(self)
