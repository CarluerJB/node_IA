from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodeeditor.node_content_conf import *
from nodeeditor.node_node_custom import *
from nodeeditor.utils import dumpException
from nodeeditor.Node_type_conf import *
from nodeeditor.node_socket import LEFT_BOTTOM, LEFT_CENTER, LEFT_TOP, RIGHT_BOTTOM, RIGHT_CENTER, RIGHT_TOP
import numpy as np
import ast

class CustomInputContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('1', self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_INPUT)
class CustomNode_Input(CustomNode):
    icon = "nodeeditor/images/input.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label = "In"
    content_label_objname = "custom_node_input"
    def __init__(self, scene):
        super().__init__(scene,inputs=[], outputs=[1])
        self.scene.addInputs(self)

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25

        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True
        self.input_can_be_added=False
        self.output_can_be_added=False
        
    
    def initInnerClasses(self):
        self.content=CustomInputContent(self)
        self.grNode=CustomGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)
    
    def initCompatible_InOut(self):
        self.node_type=INPUT_NODE_TYPE
        self.compat_input=[]
        self.compat_output=[OUTPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
    
    def evalImplementation(self):
        u_value = self.content.edit.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value

class CustomSliderContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setObjectName(self.node.content_label_objname)
        self.setLayout(self.layout)
        self.layout.addWidget(self.slider, Qt.AlignLeft)

@register_node(OP_NODE_SLIDER)
class CustomNode_Slider(CustomNode):
    icon = ""
    op_code = OP_NODE_SLIDER
    op_title = "Slider"
    content_label = ""
    content_label_objname = "custom_node_slider"
    def __init__(self, scene):
        super().__init__(scene,inputs=[1, 1], outputs=[1])
    
    def initInnerClasses(self):
        self.content=CustomSliderContent(self)
        self.grNode=CustomGraphicsNode(self)
    

class CustomOutputContent(QDMNodeContentWidget):
    def initUI(self):
        self.lbl = QLabel('42', self)
        self.lbl.setAlignment(Qt.AlignLeft)
        self.lbl.setObjectName(self.node.content_label_objname)

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

    def initInnerClasses(self):
        self.content=CustomOutputContent(self)
        self.grNode=CustomGraphicsNode(self)
    
    def initCompatible_InOut(self):
        self.node_type=OUTPUT_NODE_TYPE
        self.compat_input=[INPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
        self.compat_output=[]
    
    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return

        self.content.lbl.setText("%d" % val)
        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        return val
    


class CustomDenseContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('1', self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_DENSE)
class CustomNode_Dense(CustomNode):
    icon = ""
    op_code = OP_NODE_DENSE
    op_title = "Dense"
    content_label = ""
    content_label_objname = "custom_node_dense"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initInnerClasses(self):
        self.content=CustomDenseContent(self)
        self.grNode=CustomGraphicsNode(self)

class CustomConcatContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('1', self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_CONCAT)
class CustomNode_Dense(CustomNode):
    icon = ""
    op_code = OP_NODE_CONCAT
    op_title = "Concat"
    content_label = ""
    content_label_objname = "custom_node_concat"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 2], outputs=[1])

    def initInnerClasses(self):
        self.content=CustomDenseContent(self)
        self.grNode=CustomGraphicsNode(self)

@register_node(OP_NODE_ADD)
class CustomNode_Add(CustomNode):
    icon = ""
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = ""
    content_label_objname = "custom_node_add"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25

        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = True
        self.output_multi_edged = False
        self.input_can_be_added=False
        self.output_can_be_added=False
        
    
    def initInnerClasses(self):
        self.grNode=CustomGraphicsNode(self)
    
    def initCompatible_InOut(self):
        self.node_type=ADD_NODE_TYPE
        self.compat_input=[INPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
        self.compat_output=[OUTPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
    
    def evalOperation(self, inputs):
        print(inputs)
        # Here check for same shape of inputs => else mark invalid + msg
        return np.sum(inputs)

@register_node(OP_NODE_PROD)
class CustomNode_Prod(CustomNode):
    icon = ""
    op_code = OP_NODE_PROD
    op_title = "Prod"
    content_label = ""
    content_label_objname = "custom_node_prod"
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25

        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = True
        self.output_multi_edged = False
        self.input_can_be_added=False
        self.output_can_be_added=False
        
    
    def initInnerClasses(self):
        self.grNode=CustomGraphicsNode(self)
    
    def initCompatible_InOut(self):
        self.node_type=PROD_NODE_TYPE
        self.compat_input=[INPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
        self.compat_output=[OUTPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
    
    def evalOperation(self, inputs):
        return np.prod(inputs)

class CustomInputShapeContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('(0,0)', self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_INPUTSHAPE)
class CustomNode_InputShape(CustomNode):
    icon = "nodeeditor/images/input.png"
    op_code = OP_NODE_INPUTSHAPE
    op_title = "inputShapes"
    content_label = ""
    content_label_objname = "custom_node_inputShape"
    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25

        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True
        self.input_can_be_added=False
        self.output_can_be_added=False
        
    
    def initInnerClasses(self):
        self.content=CustomInputShapeContent(self)
        self.grNode=CustomGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)
    
    def initCompatible_InOut(self):
        self.node_type=INPUTSHAPE_NODE_TYPE
        self.compat_input=[]
        self.compat_output=[OUTPUT_NODE_TYPE, ADD_NODE_TYPE, PROD_NODE_TYPE]
    
    def evalImplementation(self):
        u_value = self.content.edit.text()
        try:
            s_value = ast.literal_eval(u_value)
            print(s_value)
            a=np.array(s_value)
            print(a.shape[0])
        except:
            pass
        self.value = 3
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value

class CustomActivationContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("None")
        self.comboBox.addItem("elu")
        self.comboBox.addItem("softmax")
        self.comboBox.addItem("selu")
        self.comboBox.addItem("softplus")
        self.comboBox.addItem("softsign")
        self.comboBox.addItem("relu")
        self.comboBox.addItem("tanh")
        self.comboBox.addItem("sigmoid")
        self.comboBox.addItem("hard_sigmoid")
        self.comboBox.addItem("exponential")
        self.comboBox.addItem("linear")
        self.comboBox.addItem("LeakyReLu")
        self.comboBox.addItem("PReLu")
        self.comboBox.addItem("ThresholdedReLU")
        self.comboBox.setObjectName(self.node.content_label_objname)
        self.comboBox.activated[str].connect(self.style_choice)
        self.setLayout(self.layout)
        self.layout.addWidget(self.comboBox, Qt.AlignLeft)
        self.initHeight=self.node.grNode.height
    
    def style_choice(self, type_choosen):
        print(type_choosen)
        if type_choosen=="elu":
            self.lbl = QLabel('alpha : ', self)
            self.edit = QLineEdit('0.0', self)
            self.edit.setAlignment(Qt.AlignRight)
            self.edit.setObjectName(self.node.content_label_objname)
            self.layout.addWidget(self.lbl)
            self.layout.addWidget(self.edit)
            self.node.grNode.height = self.initHeight+self.edit.size().height() + self.lbl.size().height()
        elif type_choosen=="softmax":
            self.lbl = QLabel('axis : ', self)
            self.edit = QLineEdit('0', self)
            self.edit.setAlignment(Qt.AlignRight)
            self.edit.setObjectName(self.node.content_label_objname)
            self.layout.addWidget(self.lbl)
            self.layout.addWidget(self.edit)
            self.node.grNode.height = self.initHeight+self.edit.size().height() + self.lbl.size().height()

        

@register_node(OP_NODE_ACTIVATION)
class CustomNode_Activation(CustomNode):
    icon = ""
    op_code = OP_NODE_ACTIVATION
    op_title = "Activation"
    content_label = ""
    content_label_objname = "custom_node_activation"
    def __init__(self, scene):
        super().__init__(scene,inputs=[1], outputs=[1])
    
    def initInnerClasses(self):
        self.content=CustomActivationContent(self)
        self.grNode=CustomGraphicsNode(self)

    



# register_node_now(OP_NODE_INPUT, CustomNode_Input)
# register_node_now(OP_NODE_OUTPUT, CustomNode_Output)


# ADD YOUR OWN NODE HERE ! (def input and output are specified except if you want to fix them then add the construct)

# @register_node(OP_NODE_INPUT)
# class CustomNode_Input(CustomNode):
#     icon = "nodeeditor/images/input.png"
#     op_code = OP_NODE_INPUT
#     op_title = "Input"
#     content_label = "In"
    