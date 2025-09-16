from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from enum import Enum

# Your custom Python Enum class
class Detection(Enum):
    OBJECT_DETECTION = 0
    CLASSIFICATION = 1
    OTHER = 2

# A simple function that accepts an enum member
def process_detection_mode(mode):
    if mode == Detection.OBJECT_DETECTION:
        print("Processing in Object Detection mode.")
    elif mode == Detection.CLASSIFICATION:
        print("Processing in Classification mode.")
    else:
        print("Processing in Other mode.")

app = QApplication([])
window = QWidget()
button = QPushButton("Click Me", window)

# You can connect a signal to a function that uses your enum
button.clicked.connect(lambda: process_detection_mode(Detection.OBJECT_DETECTION))

window.show()
app.exec()