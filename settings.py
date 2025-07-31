from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QComboBox
from shared_timer import shared_timer

class SettingsPage(QWidget):
    def __init__(self, stack, dashboard_page):
        super().__init__()
        self.stack = stack
        self.dashboard_page = dashboard_page
        self.timer_state = shared_timer

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Pomodoro Length (min):"))
        self.duration_box = QSpinBox()
        self.duration_box.setRange(1, 120)
        self.duration_box.setValue(self.timer_state.duration // 60)
        layout.addWidget(self.duration_box)

        layout.addWidget(QLabel("Break Length (min):"))
        self.break_duration_box = QSpinBox()
        self.break_duration_box.setRange(1, 120)
        self.break_duration_box.setValue(self.timer_state.break_duration // 60)
        layout.addWidget(self.break_duration_box)

        layout.addWidget(QLabel("Distraction Detection:"))
        self.inactivity_toggle = QComboBox()
        self.inactivity_toggle.addItems(["Off", "High Sensitivity", "Medium Sensitivity", "Low Sensitivity"])
        self.inactivity_toggle.setCurrentIndex(2)  # default: Medium
        layout.addWidget(self.inactivity_toggle)

        save_btn = QPushButton("Save and Return")
        save_btn.clicked.connect(self.save_and_return)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def save_and_return(self):
        new_duration = self.duration_box.value() * 60
        new_break_duration = self.break_duration_box.value() * 60
        self.timer_state.reset(new_duration, new_break_duration)

        index = self.inactivity_toggle.currentIndex()
        if index == 0:
            self.dashboard_page.set_inactivity_settings(False, 0)
        else:
            self.dashboard_page.set_inactivity_settings(True, index)

        self.stack.setCurrentWidget(self.dashboard_page)
