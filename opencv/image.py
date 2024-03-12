import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage

# Define a QWidget subclass for video processing
class VideoProcessor(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.video_capture = None  # Video capture object
        self.timer = QTimer()  # Timer for updating frames
        self.frame_rate = 30  # Frames per second
        self.processing_enabled = False  # Flag for enabling processing
        self.threshold_value = 127  # Threshold value for processing

        # Initialize the user interface
        self.init_ui()

    def init_ui(self):
        # Create the main layout
        layout = QVBoxLayout()

        # Create a QLabel widget to display the video frames
        self.label = QLabel()
        layout.addWidget(self.label)

        # Create a QPushButton to start/stop video
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_stop_video)
        layout.addWidget(self.start_button)

        # Create a QSlider for adjusting threshold value
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(self.threshold_value)
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        layout.addWidget(self.threshold_slider)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set window title and display the widget
        self.setWindowTitle('Video Processing')
        self.show()

    # Method to start/stop video capture
    def start_stop_video(self):
        if not self.video_capture:
            # If video capture is not active, start capturing
            self.video_capture = cv2.VideoCapture(0)  # Use default webcam
            self.timer.timeout.connect(self.update_frame)  # Connect timer to update_frame method
            self.timer.start(1000 // self.frame_rate)  # Start the timer
            self.start_button.setText('Stop')  # Change button text
        else:
            # If video capture is active, stop capturing
            self.video_capture.release()  # Release the video capture
            self.video_capture = None  # Reset video capture object
            self.timer.stop()  # Stop the timer
            self.start_button.setText('Start')  # Change button text

    # Method to update the displayed frame
    def update_frame(self):
        ret, frame = self.video_capture.read()  # Read frame from video capture
        if ret:
            if self.processing_enabled:
                # If processing is enabled, convert frame to grayscale, apply threshold, and convert back to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, thresholded_frame = cv2.threshold(frame, self.threshold_value, 255, cv2.THRESH_BINARY)
                frame = cv2.cvtColor(thresholded_frame, cv2.COLOR_GRAY2RGB)
            else:
                # If processing is not enabled, keep the frame in RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to QImage
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)

            # Set the pixmap to the QLabel
            self.label.setPixmap(pixmap)

    # Method to update the threshold value
    def update_threshold(self):
        self.threshold_value = self.threshold_slider.value()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoProcessor()
    sys.exit(app.exec_())
