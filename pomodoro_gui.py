import sys
import time
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QMessageBox
)
from playsound import playsound
import threading

# Constants (in seconds)
WORK_DURATION = 25 * 60
SHORT_BREAK = 5 * 60
LONG_BREAK = 15 * 60
SESSIONS_BEFORE_LONG_BREAK = 4
ALERT_SOUND = "alert.mp3"

class PomodoroApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍅 Pomodoro Timer")
        self.setFixedSize(300, 250)
        self.session_count = 0
        self.timer_duration = WORK_DURATION
        self.timer_running = False
        self.current_mode = "Work"

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        # UI Elements
        self.label_title = QLabel("Pomodoro Timer", alignment=Qt.AlignCenter)
        self.label_title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.label_mode = QLabel(self.current_mode, alignment=Qt.AlignCenter)
        self.label_mode.setStyleSheet("font-size: 16px;")

        self.label_time = QLabel(self.format_time(self.timer_duration), alignment=Qt.AlignCenter)
        self.label_time.setStyleSheet("font-size: 36px;")

        self.start_btn = QPushButton("▶ Start")
        self.start_btn.clicked.connect(self.toggle_timer)
        self.reset_btn = QPushButton("🔁 Reset")
        self.reset_btn.clicked.connect(self.reset_timer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_mode)
        layout.addWidget(self.label_time)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.reset_btn)
        self.setLayout(layout)

    def format_time(self, secs):
        mins, secs = divmod(secs, 60)
        return f"{mins:02d}:{secs:02d}"

    def toggle_timer(self):
        if not self.timer_running:
            self.timer.start()
            self.timer_running = True
            self.start_btn.setText("⏸ Pause")
        else:
            self.timer.stop()
            self.timer_running = False
            self.start_btn.setText("▶ Resume")

    def update_timer(self):
        if self.timer_duration > 0:
            self.timer_duration -= 1
            self.label_time.setText(self.format_time(self.timer_duration))
        else:
            self.timer.stop()
            self.timer_running = False
            self.start_btn.setText("▶ Start")
            threading.Thread(target=playsound, args=(ALERT_SOUND,), daemon=True).start()
            self.handle_session_end()

    def handle_session_end(self):
        if self.current_mode == "Work":
            self.session_count += 1
            if self.session_count % SESSIONS_BEFORE_LONG_BREAK == 0:
                self.current_mode = "Long Break"
                self.timer_duration = LONG_BREAK
            else:
                self.current_mode = "Short Break"
                self.timer_duration = SHORT_BREAK
        else:
            self.current_mode = "Work"
            self.timer_duration = WORK_DURATION

        self.label_mode.setText(self.current_mode)
        self.label_time.setText(self.format_time(self.timer_duration))
        self.prompt_next_session()

    def prompt_next_session(self):
        reply = QMessageBox.question(
            self, "Continue?", "Start next session?", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.toggle_timer()
        else:
            self.label_mode.setText("Finished")
            self.label_time.setText("00:00")

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.start_btn.setText("▶ Start")
        self.current_mode = "Work"
        self.timer_duration = WORK_DURATION
        self.label_mode.setText(self.current_mode)
        self.label_time.setText(self.format_time(self.timer_duration))
        self.session_count = 0
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PomodoroApp()
    window.show()
    sys.exit(app.exec_())

