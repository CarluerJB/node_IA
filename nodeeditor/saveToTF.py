class Node(object):
    def __init__(self, ID: str, reprname: str, tfrepr: str, type: str):
        self.ID = ID
        self.reprname = reprname
        self.tfrepr = tfrepr
        self.type = type
        self.children = []
        self.depth = -1

    def computeDepth(self) -> int:
        if self.depth > -1:
            return self.depth
        elif len(self.children) == 0:
            self.depth = 0
            return self.depth

        self.depth = max([x.computeDepth() for x in self.children]) + 1
        return self.depth

    def __repr__(self):
        return "<{0} - {1} - {2}>".format(
            self.depth, self.reprname + " = " + self.tfrepr, self.children
        )


def generateNodeTree(info) -> list:
    """
    No index for now
    """
    result = []
    ItoN = {}
    OtoN = {}
    for idx, node in enumerate(info["nodes"]):
        N = Node(node["id"], "layer" + str(idx), node["tfrepr"], node["type"])
        result.append(N)
        if len(node["inputs"]) > 0:
            for inp in node["inputs"]:
                ItoN[inp["id"]] = N
        if len(node["outputs"]) > 0:
            for oup in node["outputs"]:
                OtoN[oup["id"]] = N

    for edge in info["edges"]:
        ItoN[edge["end"]].children.append(OtoN[edge["start"]])

    for node in result:
        node.computeDepth()

    result.sort(key=lambda node: node.depth)

    return result


def generateStr(nodeTree: list) -> str:
    result = "import tensorflow as tf" + "\n"
    result += "import tensorflow.keras as keras" + "\n\n"

    result += "def Model():" + "\n"

    for node in nodeTree:
        result += "\t{0} = {1}".format(node.reprname, node.tfrepr)
        if len(node.children) == 1:
            result += "({0})".format(node.children[0].reprname)
        elif len(node.children) > 1:
            result += "([{0}".format(node.children[0].reprname)
            for nn in node.children[1:]:
                result += ", {0}".format(nn.reprname)
            result += "])"
        result += "\n"

    inputs = [x for x in nodeTree if x.type == "input"]
    outputs = [x for x in nodeTree if x.type == "output"]

    print(inputs)
    print(outputs)

    result += "\treturn keras.models.Model(inputs = "
    if len(inputs) == 1:
        result += inputs[0].reprname
    elif len(inputs) > 1:
        result += "[{0}".format(inputs[0].reprname)
        for nn in inputs[1:]:
            result += ", {0}".format(nn.reprname)
        result += "]"
    result += ", outputs = "
    if len(outputs) == 1:
        result += outputs[0].reprname
    elif len(outputs) > 1:
        result += "[{0}".format(outputs[0].reprname)
        for nn in outputs[1:]:
            result += ", {0}".format(nn.reprname)
        result += "]"
    result += ")" + "\n\n"

    result += 'if __name__=="__main__":' + "\n"
    result += "\tmodel = Model()" + "\n"
    result += "\tmodel.summary()" + "\n"

    return result
