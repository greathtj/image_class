import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSettings, Slot, QSize, QRect, QPoint, Qt
from PySide6.QtGui import QPixmap, QImage

from widgets.video_stream_manager import VideoControlWidget, VideoStreamer
from widgets.annotation_manager import AnnotationWidget
from widgets.project_manager import projectManagerWidget

from main_ui import Ui_MainWindow
import qdarkstyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.my_video = None
        self.camera_index = 0
        self.frame_width = 1920
        self.frame_height = 1080

        self._init_annotation_widget()
        self._init_video_control_widget()  # Initialize controls first
        # Get the first camera and start the stream
        initial_camera_index = self.video_control_widget.get_first_camera_index()
        if initial_camera_index is not None:
            self.camera_index = initial_camera_index
            self._init_video_streamer_widget()
        else:
            self.handle_camera_error("No cameras found.")

        self._init_project_manager_widget()


    def _init_video_streamer_widget(self):
        if self.my_video and self.my_video.isRunning():
            self.my_video.stop()
            self.my_video.wait()

        self.my_video = VideoStreamer(
            camera_index=self.camera_index,
            width=self.frame_width,
            height=self.frame_height,
            parent=self
        )
        self.my_video.is_detecting = False
        self.my_video.frame_ready.connect(self.my_annotator.update_image)
        self.my_video.error_occurred.connect(self.handle_camera_error)
        self.my_video.start()

    def _init_video_control_widget(self):
        self.video_control_widget = VideoControlWidget()
        self.video_control_widget.ui.comboBoxResolutions.setCurrentIndex(3)
        self.video_control_widget.alpha_beta_changed.connect(self.update_alpha_beta_on_video)
        self.video_control_widget.switch_camera_button_clicked.connect(self.switch_camera)
        self.video_control_widget.resolution_changed.connect(self.change_resolution)
        self.ui.verticalLayoutCameraControl.addWidget(self.video_control_widget)
        self.video_control_widget.update_alpha_beta_lineEdit()

    def _init_annotation_widget(self):
        self.my_annotator = AnnotationWidget(
            # get_current_selected_class_text_func = self.my_base_line_annotator._get_current_selected_class_from_list
        )
        # self.my_annotator.annotation_added.connect(self.handle_annotation_added)
        self.ui.verticalLayoutImage.addWidget(self.my_annotator)
        self.my_annotator.set_drawing_mode(AnnotationWidget.DRAW_CENTER_SQUARE) # default no drawing

    def _init_project_manager_widget(self):
        self.my_project_manager = projectManagerWidget(
            my_annotator=self.my_annotator,
            my_video=self.my_video,
        )
        self.ui.verticalLayoutProjectManager.addWidget(self.my_project_manager)

    @Slot(int, int)
    def change_resolution(self, width, height):
        self.frame_width = width
        self.frame_height = height
        self._init_video_streamer_widget()

    @Slot(int)
    def switch_camera(self, camera_index):
        if self.my_video and self.my_video.isRunning():
            self.my_video.stop()
            self.my_video.wait()

        self.camera_index = camera_index
        self._init_video_streamer_widget()

    @Slot(float, int)
    def update_alpha_beta_on_video(self, alpha:float, beta:int):
        if self.my_video:
            self.my_video.this_alph = alpha
            self.my_video.this_beta = beta
        
    @Slot(str)
    def handle_camera_error(self, error_message: str):
        print(f"Camera Error: {error_message}")
        self.my_annotator.setText(f"Camera Error: {error_message}\nCheck camera connection or index.")
        self.my_annotator.clear()
        if self.my_video:
            self.my_video.stop()

    def closeEvent(self, event):
        if self.my_video and self.my_video.isRunning():
            print(f"Stopping VideoStreamer thread for camera {self.camera_index}...")
            self.my_video.stop()
            self.my_video.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv) # Create the QApplication instance

    stylesheet = qdarkstyle.load_stylesheet(qt_api='pyside6')
    app.setStyleSheet(stylesheet)
        
    window = MainWindow()      # Create an instance of your main window
    window.show()                # Show the window
    sys.exit(app.exec())         # Start the event loop