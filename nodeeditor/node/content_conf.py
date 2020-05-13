LISTBOX_MIMETYPE = "application/x-item"

II = 1

OP_NODE_INPUT = II
II += 1
OP_NODE_OUTPUT = II
II += 1
OP_NODE_FLATTEN = II
II += 1
OP_NODE_DENSE = II
II += 1
OP_NODE_CONCAT = II
II += 1
OP_NODE_ADD = II
II += 1
OP_NODE_PROD = II
II += 1
OP_NODE_AVERAGE = II
II += 1
OP_NODE_ACTIVATION = II
II += 1
OP_NODE_CONV1D = II
II += 1
OP_NODE_CONV2D = II
II += 1
OP_NODE_CONV3D = II
II += 1
OP_NODE_DWCONV2D = II
II += 1
OP_NODE_MAX = II
II += 1
OP_NODE_MIN = II
II += 1
OP_NODE_MAXPOOLING1D = II
II += 1
OP_NODE_MAXPOOLING2D = II
II += 1
OP_NODE_MAXPOOLING3D = II
II += 1
OP_NODE_UPSAMPLING1D = II
II += 1
OP_NODE_UPSAMPLING2D = II
II += 1
OP_NODE_UPSAMPLING3D = II
II += 1
OP_NODE_GLOBALMAXPOOLING1D = II
II += 1
OP_NODE_GLOBALMAXPOOLING2D = II
II += 1
OP_NODE_GLOBALMAXPOOLING3D = II
II += 1
OP_NODE_SQUEEZE = II
II += 1
OP_NODE_EMBEDDING = II
II += 1

CUSTOM_NODES = {}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_node_now(op_code, class_reference):
    if op_code in CUSTOM_NODES:
        raise InvalidNodeRegistration(
            "Duplicate node registration of '%s'. There is already %s"
            % (op_code, CUSTOM_NODES[op_code])
        )

    CUSTOM_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class

    return decorator


def get_class_from_opcode(op_code):
    print(op_code)
    if op_code not in CUSTOM_NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" & op_code)
    return CUSTOM_NODES[op_code]
