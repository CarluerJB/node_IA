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

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = 'keras.layers.Activation("' + self.content.comboBox.currentText() + '")'
        res['type'] = "output"
        return res

    def initInnerClasses(self):
        self.content = CustomActivationContent(self)
        self.grNode = CustomGraphicsNode(self)

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        INodes = self.getInputs()

        for node in INodes:
            if node.shape is None:
                self.markDirty(True)
                self.grNode.setToolTip("WARNING : Bad input shape !")
                self.shape = None
                return

        self.shape = np.array(INodes[0].shape)

class CustomDenseGraphic(CustomGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.height = 85


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


@register_node(OP_NODE_DENSE)
class CustomNode_Dense(CustomNode):
    icon = ""
    op_code = OP_NODE_DENSE
    op_title = "Dense"
    content_label = ""
    content_label_objname = "custom_node_dense"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = 'keras.layers.Dense(units=' + str(self.content.units.value()) + ', use_bias=' + ('True' if self.content.usebias.isChecked() else 'False') + ')'
        res['type'] = "hidden"
        return res

    def initInnerClasses(self):
        self.content = CustomDenseContent(self)
        self.grNode = CustomDenseGraphic(self)
        self.content.units.valueChanged.connect(self.evalImplementation)

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        INodes = self.getInputs()

        for node in INodes:
            if node.shape is None:
                self.markDirty(True)
                self.grNode.setToolTip("WARNING : Bad input shape !")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        if len(INodes) == 0:
            self.markInvalid(True)
            self.grNode.setToolTip("ERROR : Hidden Node with no Inputs!")
            self.shape = None
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        self.shape = np.array(INodes[0].shape)
        self.shape[-1] = self.content.units.value()
        for nn in self.getOutputs():
            nn.evalImplementation()


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

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = 'keras.layers.Concatenate()'
        res['type'] = "hidden"
        return res

    def initSettings(self):
        super().initSettings()
        self.input_multi_edged = True

    def initInnerClasses(self):
        #self.content = CustomDenseContent(self)
        self.grNode = CustomGraphicsNode(self)

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        INodes = self.getInputs()

        for node in INodes:
            if node.shape is None:
                self.markDirty(True)
                self.grNode.setToolTip("WARNING : Bad input shape !")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        if len(INodes) == 0:
            self.markInvalid(True)
            self.grNode.setToolTip("ERROR : Hidden Node with no Inputs!")
            self.shape = None
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        if len(INodes) == 1:
            self.markDirty(True)
            self.grNode.setToolTip("WARNING : Usualy needs two or more Inputs. May be an Error!")
            self.shape = np.array(INodes[0].shape)
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        firstshape = INodes[0].shape
        for node in INodes[1:]:
            print(node)
            if len(node.shape) != len(firstshape) or (node.shape[:-1] != firstshape[:-1]).any():
                self.markInvalid(True)
                self.grNode.setToolTip("ERROR : Input shape mismatch!")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        self.shape = np.array(INodes[0].shape)
        for node in INodes[1:]:
            self.shape[-1] += node.shape[-1]

        for nn in self.getOutputs():
            nn.evalImplementation()

@register_node(OP_NODE_ADD)
class CustomNode_Add(CustomNode):
    icon = ""
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = ""
    content_label_objname = "custom_node_add"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = "keras.layers.Add()"
        res['type'] = "hidden"
        return res

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = True

    def initInnerClasses(self):
        self.grNode = CustomGraphicsNode(self)

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        INodes = self.getInputs()
        print(INodes)
        for node in INodes:
            if node.shape is None:
                self.markDirty(True)
                self.grNode.setToolTip("WARNING : Bad input shape !")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        if len(INodes) == 0:
            self.markInvalid(True)
            self.grNode.setToolTip("ERROR : Hidden Node with no Inputs!")
            self.shape = None
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        if len(INodes) == 1:
            self.markDirty(True)
            self.grNode.setToolTip("WARNING : Usualy needs two or more Inputs. May be an Error!")
            self.shape = np.array(INodes[0].shape)
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        firstshape = INodes[0].shape
        for node in INodes[1:]:
            if not ((len(node.shape) == len(firstshape)) and (node.shape == firstshape).all()):
                self.markInvalid(True)
                self.grNode.setToolTip("ERROR : Input shape mismatch!")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        self.shape = np.array(INodes[0].shape)
        for nn in self.getOutputs():
            nn.evalImplementation()




@register_node(OP_NODE_PROD)
class CustomNode_Prod(CustomNode):
    icon = ""
    op_code = OP_NODE_PROD
    op_title = "Multiply"
    content_label = ""
    content_label_objname = "custom_node_prod"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = "keras.layers.Multiply()"
        res['type'] = "hidden"
        return res

    def initSettings(self):
        super().initSettings()
        self.socket_spacing = 25
        self.input_socket_position = LEFT_TOP
        self.output_socket_position = RIGHT_TOP
        self.input_multi_edged = True

    def initInnerClasses(self):
        self.grNode = CustomGraphicsNode(self)

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        INodes = self.getInputs()

        for node in INodes:
            if node.shape is None:
                self.markDirty(True)
                self.grNode.setToolTip("WARNING : Bad input shape !")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        if len(INodes) == 0:
            self.markInvalid(True)
            self.grNode.setToolTip("ERROR : Hidden Node with no Inputs!")
            self.shape = None
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        if len(INodes) == 1:
            self.markDirty(True)
            self.grNode.setToolTip("WARNING : Usualy needs two or more Inputs. May be an Error!")
            self.shape = np.array(INodes[0].shape)
            for nn in self.getOutputs():
                nn.evalImplementation()
            return

        firstshape = INodes[0].shape
        for node in INodes[1:]:
            print(node)
            if len(node.shape) != len(firstshape) or (node.shape != firstshape).any():
                self.markInvalid(True)
                self.grNode.setToolTip("ERROR : Input shape mismatch!")
                self.shape = None
                for nn in self.getOutputs():
                    nn.evalImplementation()
                return

        self.shape = np.array(INodes[0].shape)
        for nn in self.getOutputs():
            nn.evalImplementation()


class CustomInputShapeContent(QDMNodeContentWidget):
    def initUI(self):
        self.edit = QLineEdit('(0, 0)', self)
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)


@register_node(OP_NODE_INPUTSHAPE)
class CustomNode_Input(CustomNode):
    icon = "nodeeditor/images/input.png"
    op_code = OP_NODE_INPUTSHAPE
    op_title = "Input"
    content_label = ""
    content_label_objname = "custom_node_inputShape"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])
        self.shape = None
        self.evalImplementation()

    def codealize(self):
        res = super().codealize()
        res['tfrepr'] = "keras.layers.Input(" + self.content.edit.text() + ")"
        res['type'] = "input"
        return res

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

    def evalImplementation(self):

        self.markInvalid(False)
        self.markDirty(False)
        self.grNode.setToolTip("")

        try:
            s_value = ast.literal_eval(self.content.edit.text())
            self.shape = np.array(s_value)
        except:
            self.shape = None
            self.markInvalid(True)
            self.grNode.setToolTip("ERROR : Invalid shape !")

        for nn in self.getOutputs():
            nn.evalImplementation()


class CustomActivationContent(QDMNodeContentWidget):
    def initUI(self):
        self.layout = QVBoxLayout()
        self.comboBox = QComboBox(self)
        # self.comboBox.addItem("None")
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
        # self.initHeight=self.node.grNode.height

    def style_choice(self, type_choosen):
        print(type_choosen)
        if type_choosen == "elu":
            self.lbl = QLabel('alpha : ', self)
            self.edit = QLineEdit('0.0', self)
            self.edit.setAlignment(Qt.AlignRight)
            self.edit.setObjectName(self.node.content_label_objname)
            self.layout.addWidget(self.lbl)
            self.layout.addWidget(self.edit)
            self.node.grNode.height = self.initHeight+self.edit.size().height() + \
                self.lbl.size().height()
        elif type_choosen == "softmax":
            self.lbl = QLabel('axis : ', self)
            self.edit = QLineEdit('0', self)
            self.edit.setAlignment(Qt.AlignRight)
            self.edit.setObjectName(self.node.content_label_objname)
            self.layout.addWidget(self.lbl)
            self.layout.addWidget(self.edit)
            self.node.grNode.height = self.node.grNode.height + \
                self.edit.size().height() + self.lbl.size().height()


@register_node(OP_NODE_ACTIVATION)
class CustomNode_Activation(CustomNode):
    icon = ""
    op_code = OP_NODE_ACTIVATION
    op_title = "Activation"
    content_label = ""
    content_label_objname = "custom_node_activation"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])

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
