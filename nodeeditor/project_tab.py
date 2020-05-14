import os
import json
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QPushButton
from nodeeditor.node.editor_tab import NodeEditorTabs
from data.image_annotation.windows import AnnotationTool


class ProjectTabs(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.project_tab = QWidget()
        self.data_tab = AnnotationTool(self)
        self.training_tab = QWidget()
        self.model_tab = NodeEditorTabs(self)
        self.deployment_tab = QWidget()

        # add all tab to tabs list
        self.tabs.addTab(self.project_tab, "Project")
        self.tabs.addTab(self.data_tab, "Data")
        self.tabs.addTab(self.training_tab, "Training")
        self.tabs.addTab(self.model_tab, "Models")
        self.tabs.addTab(self.deployment_tab, "Deployment")

        # create def_tab for non implementend tabs
        self.create_def_tabs(self.project_tab)
        self.create_def_tabs(self.data_tab)
        self.create_def_tabs(self.training_tab)
        self.create_def_tabs(self.deployment_tab)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def create_def_tabs(self, tab):
        tab.layout = QVBoxLayout()
        self.pushButton1 = QPushButton("PyQt5 button")
        tab.layout.addWidget(self.pushButton1)
        tab.setLayout(tab.layout)
