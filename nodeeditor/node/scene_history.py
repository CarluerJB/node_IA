# -*- coding: utf-8 -*-
"""
A module containing all code for working with History (Undo/Redo)
"""
from nodeeditor.node.graphics_edge import QDMGraphicsEdge
from nodeeditor.utils import dumpException

DEBUG = False


class SceneHistory:
    """Class contains all the code for undo/redo operations"""

    def __init__(self, scene: "Scene"):
        """
        :param scene: Reference to the :class:`~nodeeditor.node.scene.Scene`
        :type scene: :class:`~nodeeditor.node.scene.Scene`

        :Instance Attributes:

        - **scene** - reference to the :class:`~nodeeditor.node.scene.Scene`
        - **history_limit** - number of history steps that can be stored
        """
        self.scene = scene

        self.clear()
        self.history_limit = 32

        # listeners
        self._history_modified_listeners = []
        self._history_stored_listeners = []
        self._history_restored_listeners = []

    def clear(self):
        """Reset the history stack"""
        self.history_stack = []
        self.history_current_step = -1

    def storeInitialHistoryStamp(self):
        """Helper function usually used when new or open file requested"""
        self.storeHistory("Initial History Stamp")

    def addHistoryModifiedListener(self, callback: "function"):
        """
        Register callback for `HistoryModified` event

        :param callback: callback function
        """
        self._history_modified_listeners.append(callback)

    def addHistoryStoredListener(self, callback: "function"):
        """
        Register callback for `HistoryStored` event

        :param callback: callback function
        """
        self._history_stored_listeners.append(callback)

    def addHistoryRestoredListener(self, callback: "function"):
        """
        Register callback for `HistoryRestored` event

        :param callback: callback function
        """
        self._history_restored_listeners.append(callback)

    def canUndo(self) -> bool:
        """Return ``True`` if Undo is available for current `History Stack`

        :rtype: ``bool``
        """
        return self.history_current_step > 0

    def canRedo(self) -> bool:
        """
        Return ``True`` if Redo is available for current `History Stack`

        :rtype: ``bool``
        """
        return self.history_current_step + 1 < len(self.history_stack)

    def undo(self):
        """Undo operation"""
        if DEBUG:
            print("UNDO")

        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def redo(self):
        """Redo operation"""
        if DEBUG:
            print("REDO")
        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def restoreHistory(self):
        """
        Restore `History Stamp` from `History stack`.

        Triggers:

        - `History Modified` event
        - `History Restored` event
        """
        if DEBUG:
            print(
                "Restoring history",
                ".... current_step: @%d" % self.history_current_step,
                "(%d)" % len(self.history_stack),
            )
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])
        for callback in self._history_modified_listeners:
            callback()
        for callback in self._history_restored_listeners:
            callback()

    def storeHistory(self, desc: str, setModified: bool = False):
        """
        Store History Stamp into History Stack

        :param desc: Description of current History Stamp
        :type desc: ``str``
        :param setModified: if ``True`` marks :class:`~nodeeditor.node.scene.Scene` with `has_been_modified`
        :type setModified: ``bool``

        Triggers:

        - `History Modified`
        - `History Stored`
        """
        if setModified:
            self.scene.has_been_modified = True

        if DEBUG:
            print(
                "Storing history",
                '"%s"' % desc,
                ".... current_step: @%d" % self.history_current_step,
                "(%d)" % len(self.history_stack),
            )

        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step != -1:
            self.history_stack = self.history_stack[:(self.history_current_step+1)]

        # history is outside of the limits

        #self.history_stack = self.history_stack[1:]
        #self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step = -1

        if DEBUG:
            print("  -- setting step to:", self.history_current_step)

        # always trigger history modified (for i.e. updateEditMenu)
        for callback in self._history_modified_listeners:
            callback()
        for callback in self._history_stored_listeners:
            callback()

    def createHistoryStamp(self, desc: str) -> dict:
        """
        Create History Stamp. Internally serialize whole scene and current selection

        :param desc: Descriptive label for the History Stamp
        :return: History stamp serializing state of `Scene` and current selection
        :rtype: ``dict``
        """
        sel_obj = {
            "nodes": [],
            "edges": [],
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, "node"):
                sel_obj["nodes"].append(item.node.id)
            elif isinstance(item, QDMGraphicsEdge):
                sel_obj["edges"].append(item.edge.id)

        history_stamp = {
            "desc": desc,
            "snapshot": self.scene.serialize(),
            "selection": sel_obj,
        }

        return history_stamp

    def restoreHistoryStamp(self, history_stamp: dict):
        """
        Restore History Stamp to current `Scene` with selection of items included

        :param history_stamp: History Stamp to restore
        :type history_stamp: ``dict``
        """
        if DEBUG:
            print("RHS: ", history_stamp["desc"])

        try:
            self.scene.deserialize(history_stamp["snapshot"])

            # restore selection
            for edge_id in history_stamp["selection"]["edges"]:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.grEdge.setSelected(True)
                        break

            for node_id in history_stamp["selection"]["nodes"]:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.grNode.setSelected(True)
                        break

        except Exception as e:
            dumpException(e)

    def get_last_created_nodes_from_position(self, position):
        # renvoi la liste des noeuds + la position de la derniere creation de noeud

        # si position == None on renvoi None, None
        if position is None:
            return None, None

        # A chaque étape:
        #   - on check si position est positive:
        #   - on check si on est bien un CREATE NODE
        #       - Si oui : on renvois la liste des nodes + notre position
        #       - Si non : on décrémente position
        while position + len(self.history_stack) >= 0:
            if self.history_stack[position]['desc'].startswith("Create node"):
                return [node["id"] for node in self.history_stack[position]["snapshot"]["nodes"]], position
            else:
                position -= 1

        return None, None

    def get_last_placed_node_impl(self, position):
        if position is None:
            return None, None

        # recuperer le dernier "CREATE NODE" idD
        idD, pos = self.get_last_created_nodes_from_position(position)
        print(idD)
        print(pos)

        # 3eme cas : idD == None (=> idA == None)
        #   -   on renvoi None
        if idD is None:
            return None, None

        # recuperer l'avant-dernier "CREATE NODE" idA
        idA, _ = self.get_last_created_nodes_from_position(pos-1)
        print(idA)
        print(_)

        # 2eme cas : idD != None & idA == None
        #   -   on renvoi le node associé au seul element de idD
        if idA is None:
            for node in self.scene.nodes:
                if node.id == idD[0]:
                    return node, None

        # 1er cas : idD != None & idA != None
        #   -   on renvoi le node associé à l'élément dans idD qui n'est pas dans idA
        ID = list(set(idD) - set(idA))[0]
        for node in self.scene.nodes:
            if node.id == ID:
                return node, _

        return None, _


    def get_last_placed_node(self):
        if not self.history_stack:
            return None

        ID = None
        pos = self.history_current_step
        while ID is None and pos is not None:
            ID, pos = self.get_last_placed_node_impl(pos)
        return ID
