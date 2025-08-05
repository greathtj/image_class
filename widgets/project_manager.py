import json
import os
from PySide6.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QTableWidget, QMessageBox
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QPixmap
import time
import datetime
import random
import shutil

from widgets.project_manager_ui import Ui_FormProjectManager
from widgets.create_project_dialog import CreateProjectDialog
from widgets.annotation_manager import AnnotationWidget
from widgets.video_stream_manager import VideoStreamer

from image_classifer import image_classifier


class projectManagerWidget(QWidget):
    alpha_beta_changed = Signal(float, int)
    switch_camera_button_clicked = Signal(int)
    resolution_changed = Signal(int, int)

    def __init__(
            self, 
            my_annotator: AnnotationWidget,
            my_video: VideoStreamer,
            parent=None
        ):
        super().__init__(parent)

        self.ui = Ui_FormProjectManager()
        self.ui.setupUi(self)

        self.my_annotator = my_annotator
        self.my_video = my_video

        self.project_data = None
        self.ui.stackedWidgetProject.setCurrentIndex(0)

        self.ui.tabWidgetIC.setCurrentIndex(0)

        self.ui.pushButtonCreateProject.clicked.connect(self.open_create_project_dialog)
        self.ui.pushButtonOpenProject.clicked.connect(self.open_project_file)

    def open_create_project_dialog(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec():
            self.project_data = dialog.get_project_data()
            project_name = self.project_data.get("name")
            project_dir = self.project_data.get("directory")

            if project_name and project_dir:
                # Create the directory if it doesn't exist
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)

                # file_path = os.path.join(project_dir, f"{project_name}.json")
                file_path = f"projects/{project_name}.json"
                with open(file_path, 'w') as f:
                    json.dump(self.project_data, f, indent=4)
                print(f"Project data saved to {file_path}")

                self.ui.labelCurrentProject.setText(project_name)

                self.set_proejct_screen(self.project_data.get("type"))

    def open_project_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Project", "projects", "JSON Files (*.json)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                self.project_data = json.load(f)
            print(f"Project data loaded from {fileName}")
            print(self.project_data)

            self.ui.labelCurrentProject.setText(self.project_data.get("name"))
            project_type = self.project_data.get("type")
            self.set_proejct_screen(project_type)

    def set_proejct_screen(self, project_type):
        if project_type == "Object Detection":
            self.ui.stackedWidgetProject.setCurrentIndex(1)
        elif project_type == "Image Classification":
            self.ui.stackedWidgetProject.setCurrentIndex(2)
            self.image_classifier = image_classifier(
                parentui=self.ui,
                projec_data=self.project_data, 
                my_annotator=self.my_annotator,
                my_video=self.my_video,
                parent=self
            )
            self.image_classifier.update_file_list()
        else:
            self.ui.stackedWidgetProject.setCurrentIndex(0)

