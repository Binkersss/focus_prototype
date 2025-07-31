from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from shared_timer import shared_timer
from inactivity import get_idle_time
import subprocess

class DashboardPage(QWidget):
    def __init__(self, stack, settings_page):
        super().__init__()
        self.stack = stack
        self.settings_page = settings_page
        self.timer_state = shared_timer

        layout = QVBoxLayout()

        self.mode_label = QLabel("Focus Mode")
        layout.addWidget(self.mode_label)

        self.timer_label = QLabel("25:00")
        layout.addWidget(self.timer_label)

        self.distracted_label = QLabel("")
        layout.addWidget(self.distracted_label)

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.timer_state.start)
        layout.addWidget(start_btn)

        stop_btn = QPushButton("Pause")
        stop_btn.clicked.connect(self.timer_state.stop)
        layout.addWidget(stop_btn)

        def handle_reset():
            self.timer_state.reset()
            self.update_mode(self.timer_state.mode)

        reset_btn = QPushButton("Reset Pomodoro")
        reset_btn.clicked.connect(handle_reset)
        layout.addWidget(reset_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        layout.addWidget(settings_btn)

        # Debug Distraction Button
        debug_btn = QPushButton("Debug Distraction")
        debug_btn.clicked.connect(self.trigger_distraction)
        layout.addWidget(debug_btn)

        self.timer_state.tick.connect(self.update_time)
        self.timer_state.mode_changed.connect(self.update_mode)

        self.setLayout(layout)
        self.update_time(self.timer_state.remaining)
        self.update_mode(self.timer_state.mode)

        # Inactivity checker
        self.sensitivity_seconds = 120  # default: medium
        self.inactivity_enabled = True
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.check_inactivity)
        self.inactivity_timer.start(5000)

    def check_inactivity(self):
        if not self.inactivity_enabled:
            self.distracted_label.setText("")
            return

        idle_time = get_idle_time()
        if idle_time >= self.sensitivity_seconds:
            self.trigger_distraction()
        else:
            self.distracted_label.setText("")

    def trigger_distraction(self):
        self.distracted_label.setText("You're distracted – Take a 1 min break")
        try:
            subprocess.run(["notify-send", "You're distracted", "Take a 1 min break"])
        except Exception as e:
            print(f"Notification error: {e}")

    def update_time(self, seconds):
        m, s = divmod(seconds, 60)
        self.timer_label.setText(f"{m:02}:{s:02}")

    def update_mode(self, mode):
        self.mode_label.setText("Focus Mode" if mode == 'focus' else "Break Mode")

    def set_inactivity_settings(self, enabled: bool, sensitivity_level: int):
        self.inactivity_enabled = enabled
        if sensitivity_level == 1:
            self.sensitivity_seconds = 60    # High sensitivity
        elif sensitivity_level == 2:
            self.sensitivity_seconds = 120   # Medium
        elif sensitivity_level == 3:
            self.sensitivity_seconds = 180   # Low
