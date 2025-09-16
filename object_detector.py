import os
import time
import datetime
import shutil
from enum import Enum

from PySide6.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QTableWidget, QMessageBox
from PySide6.QtCore import QThread, Signal, QTimer

from widgets.project_manager_ui import Ui_FormProjectManager
from widgets.annotation_manager import AnnotationWidget
from widgets.annotate_dialog import AnnotateDialog
from widgets.video_stream_manager import VideoStreamer

class object_detector():
    
    def __init__(
            self, 
            parentui: Ui_FormProjectManager,
            projec_data, 
            my_annotator: AnnotationWidget,
            my_video: VideoStreamer,
            parent=None
        ):

        self.project_data = projec_data
        self.my_annotator = my_annotator
        self.my_video = my_video
        self.my_parent = parent

        self.capture_timer = QTimer(self.my_parent)
        self.capture_timer.setInterval(200)  # 0.2 seconds
        self.capture_timer.timeout.connect(self.take_shot)

        self.ui = parentui
        self.ui.pushButtonTakeShotsOD.pressed.connect(self.start_taking_shots)
        self.ui.pushButtonTakeShotsOD.released.connect(self.stop_taking_shots)
        self.ui.pushButtonTakeShotsOD.clicked.connect(self.take_shot)

        self.ui.pushButtonImpotrOD.clicked.connect(self.import_images)

        self.ui.pushButtonAnnotateOD.clicked.connect(self.start_annotation)

    def start_annotation(self):
        my_annotate_dialog = AnnotateDialog(
            project_data=self.project_data,
            detection_type="OD",
            annotation_type=AnnotationWidget.DRAW_RECTANGLE,
            parent=self.my_parent
        )
        my_annotate_dialog.exec()

    def import_images(self):
        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")
                return

            file_paths, _ = QFileDialog.getOpenFileNames(
                self.my_parent,
                "Import Images",
                "",
                "Images (*.png *.jpg *.jpeg)"
            )

            if file_paths:
                for file_path in file_paths:
                    try:
                        shutil.copy(file_path, data_dir)
                    except shutil.Error as e:
                        print(f"Error copying file: {e}")
                
                self.update_file_list()

    def start_taking_shots(self):
        self.capture_timer.start()

    def stop_taking_shots(self):
        self.capture_timer.stop()

    def take_shot(self):
        if self.project_data and self.my_annotator:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            if data_dir and os.path.exists(data_dir):
                pixmap = self.my_annotator.current_pixmap
                # timestamp = int(time.time() * 1000)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                file_path = os.path.join(data_dir, f"shot_{timestamp}.jpg")
                pixmap.save(file_path, "JPG")
                print(f"Image saved to {file_path}")
                self.update_file_list()

    def update_file_list(self):
        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            if data_dir and os.path.exists(data_dir):
                files = sorted([f for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
                self.ui.tableWidgetFilesOD.setRowCount(len(files))
                self.ui.tableWidgetFilesOD.setColumnCount(2)
                self.ui.tableWidgetFilesOD.setHorizontalHeaderLabels(["File Name", "Class"])
                self.ui.tableWidgetFilesOD.setColumnWidth(0, 250)
                self.ui.tableWidgetFilesOD.setColumnWidth(1, 60)
                for row, file_name in enumerate(files):
                    self.ui.tableWidgetFilesOD.setItem(row, 0, QTableWidgetItem(file_name))
                    self.ui.tableWidgetFilesOD.setItem(row, 1, QTableWidgetItem(""))
