import sys
import time
import io
import contextlib
import argparse

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QProgressBar
)
from PySide6.QtCore import QObject, Signal, QThread, Slot

# --- STEP 1: Output Redirection Class ---
# This class redirects stdout/stderr and emits a signal with the captured text.
class StreamRedirector(QObject):
    text_written = Signal(str)

    def write(self, text):
        self.text_written.emit(text)

    def flush(self):
        # This method is required by the file-like object interface
        pass

# --- STEP 2: Worker Class for the Background Thread ---
# This object contains the long-running task (the YOLO training).
class YOLOv8Worker(QObject):
    finished = Signal()
    progress_signal = Signal(int)

    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.is_running = True

        self.args = args

    def run_training(self):
        """
        Simulates the YOLO training process.
        In a real application, you would put your YOLO code here.
        """
        if not self.is_running: return

        print("Starting YOLOv8 training process...")
        
        # Placeholder for the actual YOLO training code
        from ultralytics import YOLO
        model = YOLO(self.args.model)
        model.train(
            data=self.args.data, 
            epochs=self.args.epochs,
            imgsz=self.args.imgsz,
            project=self.args.project,
            name=self.args.name
        )
        
        # for epoch in range(1, 11):
        #     if not self.is_running:
        #         print("Training stopped prematurely.")
        #         break
            
        #     time.sleep(0.5) # Simulate work
        #     print(f"Epoch {epoch}/10: Training in progress...")
        #     self.progress_signal.emit(epoch * 10) # Emit progress signal
        
        print("YOLOv8 training finished.")
        self.finished.emit() # Signal that the task is complete

    def stop(self):
        self.is_running = False

# --- STEP 3: Main GUI Application ---
class YOLOv8GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 Training GUI")
        self.setGeometry(100, 100, 700, 500)
        
        self.thread = None
        self.worker = None
        self.is_thread_active = False

        self.init_ui()
        self.parse_the_arguments()

    def parse_the_arguments(self):
        parser = argparse.ArgumentParser(description="A simple data processing script.")
        # 2. Add arguments to the parser
        # Positional argument (required)
        # parser.add_argument(
        #     "input_file",
        #     type=str,
        #     help="Path to the input file to be processed."
        # )

        # # Optional argument with a default value
        # parser.add_argument(
        #     "--output_file",
        #     type=str,
        #     default="output.txt",
        #     help="Path to the output file (default: output.txt)."
        # )

        # dataset
        parser.add_argument(
            "--data",
            type=str,
            default="",
            help="dataset path"
        )

        # Optional argument with a specific type
        parser.add_argument(
            "--model",
            type=str,
            default="yolov8n-cls.pt",
            help="pretrained model such as yolov8n-cls.pt or of that kind"
        )

        # Optional argument with a specific type
        parser.add_argument(
            "--epochs",
            type=int,
            default=100,
            help="number of train epochs (default 100)"
        )

        # Optional argument with a specific type
        parser.add_argument(
            "--imgsz",
            type=int,
            default="640",
            help="target image size to be converted (default 640)"
        )

        # Optional argument with a specific type
        parser.add_argument(
            "--project",
            type=str,
            default="",
            help="Name of the project directory where training outputs are saved."
        )

        # Optional argument with a specific type
        parser.add_argument(
            "--name",
            type=str,
            default="",
            help="Name of the training run. Used for creating a subdirectory within the project folder, where training logs and outputs are stored."
        )


        # 3. Parse the arguments
        self.args = parser.parse_args()
        
        if self.args.data == "":
            print("No data is specified.")
        elif self.args.model == "":
            print("No pretrained model is given.")
        elif self.args.epochs == 0:
            print("Epoch is not specified.")
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.status_label = QLabel("Status: Ready to train.")
        layout.addWidget(self.status_label)
        
        # self.progress_bar = QProgressBar()
        # self.progress_bar.setRange(0, 100)
        # self.progress_bar.setValue(0)
        # layout.addWidget(self.progress_bar)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        self.start_button = QPushButton("Start YOLOv8 Training")
        self.start_button.clicked.connect(self.start_training)
        layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Training")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_training)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
        
        # Create the stream redirector and store original stdout
        self.stream_redirector = StreamRedirector()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
        # Connect the redirection signal to our update slot
        self.stream_redirector.text_written.connect(self.update_log)
        
    @Slot()
    def start_training(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.log_output.clear()
        self.status_label.setText("Status: Training in progress...")
        # self.progress_bar.setValue(0)

        # Redirect stdout and stderr to our custom stream
        sys.stdout = self.stream_redirector
        sys.stderr = self.stream_redirector

        # Create a QThread and Worker object
        self.thread = QThread()
        self.worker = YOLOv8Worker(self.args)
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run_training)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.training_finished)
        # self.worker.progress_signal.connect(self.progress_bar.setValue)
        
        # Clean up when the thread finishes
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread
        self.thread.start()

    @Slot()
    def stop_training(self):
        if self.thread is not None:
            self.worker.stop()
            self.status_label.setText("Status: Stopping training...")

    @Slot()
    def training_finished(self):
        self.status_label.setText("Status: Training complete!")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        # Restore original stdout and stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    @Slot(str)
    def update_log(self, text):
        # 1. Append the new text
        self.log_output.insertPlainText(text)

        # 2. Get the vertical scroll bar
        v_scrollbar = self.log_output.verticalScrollBar()

        # 3. Set its value to the maximum (i.e., scroll to the bottom)
        v_scrollbar.setValue(v_scrollbar.maximum())

    def closeEvent(self, event):
        # Now, check the state flag instead of a method call
        if self.is_thread_active:
            self.stop_training()
            # Wait for the thread to terminate.
            # This is safe because we have explicitly checked the flag.
            if self.thread is not None:
                self.thread.wait()
            
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOv8GUI()
    window.show()
    sys.exit(app.exec())