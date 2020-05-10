import os
import sys
import inspect
from PyQt5.QtWidgets import *

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from nodeeditor.utils import loadStylesheet
from nodeeditor.node.editor_window import NodeEditorWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = NodeEditorWindow()
    wnd.tabs_project.model_tab.nodeEditor.addNodes()
    module_path = os.path.dirname(inspect.getfile(wnd.__class__))

    loadStylesheet(os.path.join(module_path, "qss/nodestyle.qss"))

    sys.exit(app.exec_())
