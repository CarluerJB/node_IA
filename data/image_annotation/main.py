import os
import sys
from PyQt5.QtWidgets import *

from windows import AnnotationEditorWindow



if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = AnnotationEditorWindow()

    sys.exit(app.exec_())
