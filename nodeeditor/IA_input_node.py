from PyQt5.QtCore import *
from PyQt5.QtGui import *
from nodeeditor.node_content_conf import *
from nodeeditor.node_node_custom import *
from nodeeditor.utils import dumpException
from nodeeditor.Node_type_conf import *
from nodeeditor.node_socket import LEFT_BOTTOM, LEFT_CENTER, LEFT_TOP, RIGHT_BOTTOM, RIGHT_CENTER, RIGHT_TOP
import numpy as np
import ast


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
        self.tfrepr = 'keras.layers.Activation("' + self.content.activation.currentText() + '")'

    def initInnerClasses(self):
        self.content = CustomActivationContent(self)
        self.grNode = CustomGraphicsNode(self)




class CustomDenseGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 105
        self.width = 170

class CustomDenseContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Units :", self)
        self.HL.addWidget(self.label)
        self.units = QSpinBox(self)
        self.units.setMinimum(1)
        self.units.setMaximum(2147483647)
        self.units.setAlignment(Qt.AlignRight)
        self.units.setObjectName(self.node.content_label_objname)
        self.HL.addWidget(self.units)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Use bias ? :", self)
        self.HL2.addWidget(self.label2)
        self.usebias = QCheckBox(self)
        self.usebias.setChecked(True)
        self.HL2.addWidget(self.usebias)

        self.VL.addLayout(self.HL2)

        self.HL5 = QHBoxLayout(self)
        self.label5 = QLabel("Activation :", self)
        self.HL5.addWidget(self.label5)
        self.activation = QComboBox(self)
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("relu")
        self.activation.addItem("tanh")
        self.activation.addItem("sigmoid")
        self.activation.addItem("hard_sigmoid")
        self.activation.addItem("exponential")
        self.HL5.addWidget(self.activation)

        self.VL.addLayout(self.HL5)

@register_node(OP_NODE_DENSE)
class CustomNode_Dense(CustomNode):
    icon = ""
    op_code = OP_NODE_DENSE
    op_title = "Dense"
    content_label = ""
    content_label_objname = "custom_node_dense"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = 'keras.layers.Dense(units=' + str(self.content.units.value()) + \
            ', use_bias=' + ('True' if self.content.usebias.isChecked() else 'False') + \
            ', activation="' + self.content.activation.currentText() + '"' + \
            ')'

    def initInnerClasses(self):
        self.content = CustomDenseContent(self)
        self.grNode = CustomDenseGraphic(self)
        self.content.units.valueChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()
        self.shape = np.array(INodes[0].shape)
        self.shape[-1] = self.content.units.value()




class CustomConcatContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('1', self)
        self.edit.setAlignment(Qt.AlignLeft)
        self.edit.setObjectName(self.node.content_label_objname)

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
        self.tfrepr = 'keras.layers.Concatenate()'

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def initInnerClasses(self):
        #self.content = CustomDenseContent(self)
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
            if len(node.shape) != len(firstshape) or (node.shape[:-1] != firstshape[:-1]).any():
                self.addError("Input shape mismatch")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)
        for node in INodes[1:]:
            self.shape[-1] += node.shape[-1]





@register_node(OP_NODE_ADD)
class CustomNode_Add(CustomNode):
    icon = ""
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = ""
    content_label_objname = "custom_node_add"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Add()"

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
            if not ((len(node.shape) == len(firstshape)) and (node.shape == firstshape).all()):
                self.addError("Input shape mismatch")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)




@register_node(OP_NODE_PROD)
class CustomNode_Prod(CustomNode):
    icon = ""
    op_code = OP_NODE_PROD
    op_title = "Multiply"
    content_label = ""
    content_label_objname = "custom_node_prod"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Multiply()"

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
            print(node)
            if len(node.shape) != len(firstshape) or (node.shape != firstshape).any():
                self.addError("Input shape mismatch")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)




class CustomInputShapeContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('(0, 0)', self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_INPUT)
class CustomNode_Input(CustomNode):
    icon = "nodeeditor/images/input.png"
    op_code = OP_NODE_INPUT
    op_title = "Input"
    content_label = ""
    content_label_objname = "custom_node_inputShape"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])

    def setType(self):
        self.type = "input"

    def updatetfrepr(self):
        self.tfrepr = "keras.layers.Input(" + self.content.edit.text() + ")"

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = False
        self.output_multi_edged = True
        self.input_can_be_added = False
        self.output_can_be_added = False

    def initInnerClasses(self):
        self.content = CustomInputShapeContent(self)
        self.grNode = CustomGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def EvalImpl_(self):
        try:
            s_value = ast.literal_eval(self.content.edit.text())
            self.shape = np.array(s_value)
        except:
            self.shape = None
            self.addError("Invalid shape")




class CustomConv1DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 170

class CustomConv1DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Filters :", self)
        self.HL.addWidget(self.label)
        self.filters = QSpinBox(self)
        self.filters.setMinimum(1)
        self.filters.setMaximum(2147483647)
        self.filters.setAlignment(Qt.AlignRight)
        self.HL.addWidget(self.filters)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Kernel Size :", self)
        self.HL2.addWidget(self.label2)
        self.kernelsize = QSpinBox(self)
        self.kernelsize.setMinimum(1)
        self.kernelsize.setMaximum(2147483647)
        self.kernelsize.setSingleStep(1)
        self.kernelsize.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsize)

        self.VL.addLayout(self.HL2)

        self.HL3 = QHBoxLayout(self)
        self.label3 = QLabel("Strides :", self)
        self.HL3.addWidget(self.label3)
        self.strides = QSpinBox(self)
        self.strides.setMinimum(1)
        self.strides.setMaximum(2147483647)
        self.strides.setSingleStep(1)
        self.strides.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.strides)

        self.VL.addLayout(self.HL3)

        self.HL4 = QHBoxLayout(self)
        self.label4 = QLabel("Padding :", self)
        self.HL4.addWidget(self.label4)
        self.padding = QComboBox(self)
        self.padding.addItem("valid")
        self.padding.addItem("same")
        self.HL4.addWidget(self.padding)

        self.VL.addLayout(self.HL4)

        self.HL5 = QHBoxLayout(self)
        self.label5 = QLabel("Activation :", self)
        self.HL5.addWidget(self.label5)
        self.activation = QComboBox(self)
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("relu")
        self.activation.addItem("tanh")
        self.activation.addItem("sigmoid")
        self.activation.addItem("hard_sigmoid")
        self.activation.addItem("exponential")
        self.HL5.addWidget(self.activation)

        self.VL.addLayout(self.HL5)

@register_node(OP_NODE_CONV1D)
class CustomNode_Conv1D(CustomNode):
    icon = ""
    op_code = OP_NODE_CONV1D
    op_title = "Conv1D"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = 'keras.layers.Conv1D(filters=' + str(self.content.filters.value()) + \
            ', kernel_size=' + str(self.content.kernelsize.value()) + \
            ', strides=' + str(self.content.strides.value()) + \
            ', padding="' + self.content.padding.currentText() + \
            ', activation="' + self.content.activation.currentText() + '"' + \
            '")'

    def initInnerClasses(self):
        self.content = CustomConv1DContent(self)
        self.grNode = CustomConv1DGraphic(self)
        self.content.filters.valueChanged.connect(self.evalImplementation)
        self.content.kernelsize.valueChanged.connect(self.evalImplementation)
        self.content.strides.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        INodes = self.getInputs()

        if len(INodes[0].shape) != 2:
            self.addError("Conv1D need input shape of exactly size 2")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[1] = self.content.filters.value()

        self.shape[0] -= (self.content.kernelsize.value() -1) if self.content.padding.currentText() == "valid" else 0
        self.shape[0] = (self.shape[0] // self.content.strides.value()) + (1 if self.shape[0] % self.content.strides.value() != 0 else 0)




class CustomConv2DGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 160
        self.width = 255


class CustomConv2DContent(QDMNodeContentWidget):
    def initUI(self):
        self.VL = QVBoxLayout(self)

        self.HL = QHBoxLayout(self)
        self.label = QLabel("Filters :", self)
        self.HL.addWidget(self.label)
        self.filters = QSpinBox(self)
        self.filters.setMinimum(1)
        self.filters.setMaximum(2147483647)
        self.filters.setAlignment(Qt.AlignRight)
        self.HL.addWidget(self.filters)

        self.VL.addLayout(self.HL)

        self.HL2 = QHBoxLayout(self)
        self.label2 = QLabel("Kernel Size :", self)
        self.HL2.addWidget(self.label2)
        self.kernelsizex = QSpinBox(self)
        self.kernelsizex.setMinimum(1)
        self.kernelsizex.setMaximum(2147483647)
        self.kernelsizex.setSingleStep(1)
        self.kernelsizex.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizex)
        self.kernelsizey = QSpinBox(self)
        self.kernelsizey.setMinimum(1)
        self.kernelsizey.setMaximum(2147483647)
        self.kernelsizey.setSingleStep(1)
        self.kernelsizey.setAlignment(Qt.AlignRight)
        self.HL2.addWidget(self.kernelsizey)

        self.VL.addLayout(self.HL2)

        self.HL3 = QHBoxLayout(self)
        self.label3 = QLabel("Strides :", self)
        self.HL3.addWidget(self.label3)
        self.stridesx = QSpinBox(self)
        self.stridesx.setMinimum(1)
        self.stridesx.setMaximum(2147483647)
        self.stridesx.setSingleStep(1)
        self.stridesx.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.stridesx)
        self.stridesy = QSpinBox(self)
        self.stridesy.setMinimum(1)
        self.stridesy.setMaximum(2147483647)
        self.stridesy.setSingleStep(1)
        self.stridesy.setAlignment(Qt.AlignRight)
        self.HL3.addWidget(self.stridesy)

        self.VL.addLayout(self.HL3)

        self.HL4 = QHBoxLayout(self)
        self.label4 = QLabel("Padding :", self)
        self.HL4.addWidget(self.label4)
        self.padding = QComboBox(self)
        self.padding.addItem("valid")
        self.padding.addItem("same")
        self.HL4.addWidget(self.padding)

        self.VL.addLayout(self.HL4)

        self.HL5 = QHBoxLayout(self)
        self.label5 = QLabel("Activation :", self)
        self.HL5.addWidget(self.label5)
        self.activation = QComboBox(self)
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("relu")
        self.activation.addItem("tanh")
        self.activation.addItem("sigmoid")
        self.activation.addItem("hard_sigmoid")
        self.activation.addItem("exponential")
        self.HL5.addWidget(self.activation)

        self.VL.addLayout(self.HL5)

@register_node(OP_NODE_CONV2D)
class CustomNode_Conv2D(CustomNode):
    icon = ""
    op_code = OP_NODE_CONV2D
    op_title = "Conv2D"
    content_label = ""

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = 'keras.layers.Conv2D(filters=' + str(self.content.filters.value()) + \
            ', kernel_size=(' + str(self.content.kernelsizex.value()) + ', ' + str(self.content.kernelsizey.value()) + ')' + \
            ', strides=(' + str(self.content.stridesx.value()) + ', ' + str(self.content.stridesy.value()) + ')' + \
            ', padding="' + self.content.padding.currentText() + '"' + \
            ', activation="' + self.content.activation.currentText() + '"' + \
            ')'

    def initInnerClasses(self):
        self.content = CustomConv2DContent(self)
        self.grNode = CustomConv2DGraphic(self)
        self.content.filters.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizex.valueChanged.connect(self.evalImplementation)
        self.content.kernelsizey.valueChanged.connect(self.evalImplementation)
        self.content.stridesx.valueChanged.connect(self.evalImplementation)
        self.content.stridesy.valueChanged.connect(self.evalImplementation)
        self.content.padding.currentIndexChanged.connect(self.evalImplementation)

    def EvalImpl_(self):
        if self.content.kernelsizex.value() % 2 == 0:
            self.addWarning("Even kernel size at pos 1", self.content.kernelsizex, "background-color: yellow;")

        if self.content.kernelsizey.value() % 2 == 0:
            self.addWarning("Even kernel size at pos 2", self.content.kernelsizey, "background-color: yellow;")

        if self.content.kernelsizex.value() != self.content.kernelsizey.value():
            self.addWarning("Kernel size of different values", self.content.label2, "color: red;")

        if self.content.stridesx.value() != self.content.stridesy.value():
            self.addWarning("Strides of different values", self.content.label3, "color: red;")

        INodes = self.getInputs()

        if len(INodes[0].shape) != 3:
            self.addError("Conv2D need input shape of exactly size 3")
            self.shape = None
            return

        self.shape = np.array(INodes[0].shape)

        self.shape[2] = self.content.filters.value()

        if self.shape[0] != None:
            self.shape[0] -= (self.content.kernelsizex.value() -1) if self.content.padding.currentText() == "valid" else 0
            self.shape[0] = (self.shape[0] // self.content.stridesx.value()) + (1 if self.shape[0] % self.content.stridesx.value() != 0 else 0)
        else:
            self.shape[0] = None

        if self.shape[1] != None:
            self.shape[1] -= (self.content.kernelsizey.value() -1) if self.content.padding.currentText() == "valid" else 0
            self.shape[1] = (self.shape[1] // self.content.stridesy.value()) + (1 if self.shape[1] % self.content.stridesy.value() != 0 else 0)
        else:
            self.shape[1] = None

    def resetAll(self):
        super().resetAll()
        self.content.label2.setStyleSheet("color : white;")
        self.content.label2.setToolTip("")
        self.content.label3.setStyleSheet("color : white;")

        self.content.kernelsizex.setStyleSheet("background-color: white;")
        self.content.kernelsizex.setToolTip("")
        self.content.kernelsizey.setStyleSheet("background-color: white;")
        self.content.kernelsizey.setToolTip("")





class CustomActivationContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.activation = QComboBox(self)
        # self.comboBox.addItem("None")
        #self.comboBox.addItem("elu")
        self.activation.addItem("linear")
        self.activation.addItem("softmax")
        #self.comboBox.addItem("selu")
        self.activation.addItem("softplus")
        self.activation.addItem("softsign")
        self.activation.addItem("relu")
        self.activation.addItem("tanh")
        self.activation.addItem("sigmoid")
        self.activation.addItem("hard_sigmoid")
        self.activation.addItem("exponential")
        #self.comboBox.addItem("LeakyReLu")
        #self.comboBox.addItem("PReLu")
        #self.comboBox.addItem("ThresholdedReLU")
        #self.comboBox.setObjectName(self.node.content_label_objname)
        #self.comboBox.activated[str].connect(self.style_choice)
        self.setLayout(self.layout)
        self.layout.addWidget(self.activation, Qt.AlignLeft)
        # self.initHeight=self.node.grNode.height

    # def style_choice(self, type_choosen):
    #     print(type_choosen)
    #     if type_choosen == "elu":
    #         self.lbl = QLabel('alpha : ', self)
    #         self.edit = QLineEdit('0.0', self)
    #         self.edit.setAlignment(Qt.AlignRight)
    #         self.edit.setObjectName(self.node.content_label_objname)
    #         self.layout.addWidget(self.lbl)
    #         self.layout.addWidget(self.edit)
    #         self.node.grNode.height = self.initHeight+self.edit.size().height() + \
    #             self.lbl.size().height()
    #     elif type_choosen == "softmax":
    #         self.lbl = QLabel('axis : ', self)
    #         self.edit = QLineEdit('0', self)
    #         self.edit.setAlignment(Qt.AlignRight)
    #         self.edit.setObjectName(self.node.content_label_objname)
    #         self.layout.addWidget(self.lbl)
    #         self.layout.addWidget(self.edit)
    #         self.node.grNode.height = self.node.grNode.height + \
    #             self.edit.size().height() + self.lbl.size().height()


@register_node(OP_NODE_ACTIVATION)
class CustomNode_Activation(CustomNode):
    icon = ""
    op_code = OP_NODE_ACTIVATION
    op_title = "Activation"
    content_label = ""
    content_label_objname = "custom_node_activation"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def updatetfrepr(self):
        self.tfrepr = 'keras.layers.Activation("' + self.content.activation.currentText() + '")'

    def initInnerClasses(self):
        self.content = CustomActivationContent(self)
        self.grNode = CustomGraphicsNode(self)


# register_node_now(OP_NODE_INPUT, CustomNode_Input)
# register_node_now(OP_NODE_OUTPUT, CustomNode_Output)


# ADD YOUR OWN NODE HERE ! (def input and output are specified except if you want to fix them then add the construct)

# @register_node(OP_NODE_INPUT)
# class CustomNode_Input(CustomNode):
#     icon = "nodeeditor/images/input.png"
#     op_code = OP_NODE_INPUT
#     op_title = "Input"
#     content_label = "In"
