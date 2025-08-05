# functionLib/video_stream_manager.py

import cv2

from ultralytics import YOLO

from PySide6.QtCore import QThread, Signal, Slot, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QWidget, QApplication

from widgets.video_stream_manager_ui import Ui_FormCameraControl
from PySide6.QtCore import QSettings

class VideoControlWidget(QWidget):
    alpha_beta_changed = Signal(float, int)
    switch_camera_button_clicked = Signal(int)
    resolution_changed = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_FormCameraControl()
        self.ui.setupUi(self)
        
        self.ui.lineEditAlpha.setText(str(float(self.ui.horizontalSliderAlpha.value()/10)))
        self.ui.lineEditBeta.setText(str(self.ui.horizontalSliderBeta.value()))

        self.ui.horizontalSliderAlpha.valueChanged.connect(self.update_alpha_beta_lineEdit)
        self.ui.horizontalSliderBeta.valueChanged.connect(self.update_alpha_beta_lineEdit)
        self.ui.lineEditAlpha.textChanged.connect(self.update_alpha_beta_slider)
        self.ui.lineEditBeta.textChanged.connect(self.update_alpha_beta_slider)

        self.ui.pushButtonSwitchCamera.clicked.connect(self.on_switch_camera_clicked)
        self.ui.pushButtonApplyResolution.clicked.connect(self.on_apply_resolution_clicked)

        self.populate_camera_list()
        self.populate_resolutions()

    def populate_resolutions(self):
        resolutions = [
            (640, 480),
            (800, 600),
            (1280, 720),
            (1920, 1080),
        ]
        for w, h in resolutions:
            self.ui.comboBoxResolutions.addItem(f"{w}x{h}", userData=(w, h))

    def on_apply_resolution_clicked(self):
        w, h = self.ui.comboBoxResolutions.currentData()
        self.resolution_changed.emit(w, h)

    def populate_camera_list(self):
        """Detects available cameras and populates the combo box."""
        self.ui.comboBoxCameras.clear()
        available_cameras = self.get_available_cameras()
        for index, name in available_cameras.items():
            self.ui.comboBoxCameras.addItem(f"{name} ({index})", userData=index)

    def get_available_cameras(self):
        """Returns a dictionary of available camera indices and their names."""
        available_cameras = {}
        for i in range(10):  # Check up to 10 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras[i] = f"Camera {i}"
                cap.release()
        return available_cameras

    def on_switch_camera_clicked(self):
        camera_index = self.ui.comboBoxCameras.currentData()
        if camera_index is not None:
            self.switch_camera_button_clicked.emit(camera_index)

    def get_first_camera_index(self):
        """Returns the index of the first camera in the combo box, or None if empty."""
        if self.ui.comboBoxCameras.count() > 0:
            return self.ui.comboBoxCameras.itemData(0)
        return None

    def _load_settings(self, settings):
        if settings == None:
            return
        
        """저장된 설정을 로드하고 위젯에 적용합니다."""
        # settings = QSettings() # QSettings 객체 생성 (앞서 설정한 조직/앱 이름을 사용)

        alpha = settings["Camera_alpha"] if "Camera_alpha" in settings else 1.5
        self.ui.lineEditAlpha.setText(str(alpha))

        beta = settings["Camera_beta"] if "Camera_beta" in settings else 0
        self.ui.lineEditBeta.setText(str(beta))

    def update_alpha_beta_lineEdit(self):
        alpha = float(self.ui.horizontalSliderAlpha.value()/10)
        beta = self.ui.horizontalSliderBeta.value()

        self.ui.lineEditAlpha.setText(str(alpha))
        self.ui.lineEditBeta.setText(str(beta))

        self.alpha_beta_changed.emit(alpha, beta)

    def update_alpha_beta_slider(self):
        alpha = int(float(self.ui.lineEditAlpha.text()) * 10 )
        beta = int(self.ui.lineEditBeta.text())

        self.ui.horizontalSliderAlpha.setValue(alpha)
        self.ui.horizontalSliderBeta.setValue(beta)

        self.alpha_beta_changed.emit(float(alpha/10), beta)

    def _get_current_input_selections(self):
        current_settings = {}
        current_settings["Camera_alpha"] = float(self.ui.lineEditAlpha.text())
        current_settings["Camera_beta"] = int(self.ui.lineEditBeta.text())

        return current_settings

class VideoStreamer(QThread):
    """
    A QThread to continuously capture frames from a camera and emit them.
    """
    frame_ready = Signal(QImage, QImage, object, bool)
    error_occurred = Signal(str)

    this_alph = 1.0
    this_beta = 0

    def __init__(self, camera_index=0, width=640, height=480, parent=None):
        super().__init__(parent)
        
        self.camera_index = camera_index
        self.frame_width = width
        self.frame_height = height
        self._running = True
        self.cap = None
        self.this_model = None
        self.is_detecting = False

    def set_resolution(self, width, height):
        self.frame_width = width
        self.frame_height = height
        if self.isRunning():
            self.stop()
            self.start()

    def run(self):
        self._running = True
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise IOError(f"Cannot open camera with index {self.camera_index}")

            # Request MJPEG format for potentially higher performance
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
            # print(f"width = {self.frame_width}, height = {self.frame_height}")

            while self._running and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    # Resize frame for processing to reduce computational load
                    processing_frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)

                    # Adjust brightness and contrast on the smaller frame
                    processing_frame = self.adjust_brightness_contrast_frame(processing_frame, self.this_alph, self.this_beta)
                    
                    dframe = None
                    results = None
                    qt_image = None
                    qt_dimage = None

                    # Convert the original high-res frame for display
                    display_rgb_image = cv2.cvtColor(processing_frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = display_rgb_image.shape
                    bytes_per_line = ch * w
                    qt_image = QImage(display_rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                    if self.is_detecting:
                        # Perform detection on the smaller, processed frame
                        results = self.this_model(processing_frame, verbose=False, imgsz=640)
                        # Plot results on the smaller frame
                        dframe = results[0].plot()
                        # Convert the detected frame for display
                        dframe_rgb_image = cv2.cvtColor(dframe, cv2.COLOR_BGR2RGB)
                        h, w, ch = dframe_rgb_image.shape
                        bytes_per_line = ch * w
                        qt_dimage = QImage(dframe_rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                    self.frame_ready.emit(qt_image, qt_dimage, results, False)
                else:
                    self.error_occurred.emit(f"Failed to read frame from camera {self.camera_index}")
                    break # Exit loop on read failure
                self.msleep(1)
        except Exception as e:
            self.error_occurred.emit(f"Camera stream error: {e}")
        finally:
            if self.cap and self.cap.isOpened():
                self.cap.release()
                print(f"Camera {self.camera_index} released.")
            self._running = False

    def stop(self):
        self._running = False
        self.wait() # Wait for the thread to finish gracefully

    def set_model(self, model_path:str):
        self.this_model = YOLO(model_path)

    def adjust_brightness_contrast_frame(self, frame, alpha:float=1.0, beta:int=0):
        """
        Adjusts the brightness and contrast of a single image frame.

        Args:
            frame (numpy.ndarray): The input image frame (e.g., from cv2.VideoCapture.read()).
            alpha (float): Contrast control (1.0 for no change, >1.0 for increased, <1.0 for decreased).
                        Typical range: 0.0 to 3.0.
            beta (int): Brightness control (0 for no change, >0 for increased, <0 for decreased).
                        Typical range: -127 to 127 (for 8-bit images).

        Returns:
            numpy.ndarray: The adjusted image frame.
        """
        if frame is None:
            raise ValueError("Input frame cannot be None.")

        # Apply the transformation: new_image = alpha * original_image + beta
        # cv2.convertScaleAbs handles pixel value clamping (0-255) automatically
        adjusted_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

        return adjusted_frame         