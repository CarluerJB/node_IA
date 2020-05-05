
LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_SLIDER = 3
OP_NODE_DENSE = 4
OP_NODE_CONCAT = 5
OP_NODE_ADD = 6
OP_NODE_PROD = 7
OP_NODE_INPUTSHAPE = 8
OP_NODE_ACTIVATION = 9

CUSTOM_NODES = {
}

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass

def register_node_now(op_code, class_reference):
    if op_code in CUSTOM_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(op_code, CUSTOM_NODES[op_code]))

    CUSTOM_NODES[op_code] = class_reference

def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    print(op_code)
    if op_code not in CUSTOM_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" &op_code)
    return CUSTOM_NODES[op_code]