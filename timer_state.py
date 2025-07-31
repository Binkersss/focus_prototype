from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon

import subprocess


class TimerState(QObject):
    tick = pyqtSignal(int)
    mode_changed = pyqtSignal(str)  # 'focus' or 'break'

    def __init__(self):
        super().__init__()
        self.focus_duration = 25 * 60
        self.break_duration = 5 * 60
        self.duration = self.focus_duration
        self.remaining = self.duration
        self.is_running = False
        self.mode = 'focus'

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

        # ✅ Safe tray icon creation (assumes QApplication already exists)
        # if QSystemTrayIcon.isSystemTrayAvailable():
        #     self.tray = QSystemTrayIcon()
        #     self.tray.setIcon(QIcon())  # Replace with QIcon("icon.png") if needed
        #     self.tray.setVisible(True)
        # else:
        #     self.tray = None
        #     print("System tray not available.")

    def _tick(self):
        self.remaining -= 1
        self.tick.emit(self.remaining)
        if self.remaining <= 0:
            self._notify_mode_end()
            self._switch_mode()

    def _switch_mode(self):
        if self.mode == 'focus':
            self.mode = 'break'
            self.duration = self.break_duration
        else:
            self.mode = 'focus'
            self.duration = self.focus_duration

        self.remaining = self.duration
        self.mode_changed.emit(self.mode)
        self.start()


    def _notify_mode_end(self):
        if self.mode == 'focus':
            subprocess.run(["notify-send", "Pomodoro", "Focus session ended. Break time!"])
        else:
            subprocess.run(["notify-send", "Pomodoro", "Break over. Back to focus!"])

    def start(self):
        if not self.is_running and self.remaining > 0:
            self.is_running = True
            self.timer.start(1000)

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
        self.is_running = False

    def reset(self, duration=None, break_duration=None):
        if duration is not None:
            self.focus_duration = duration
        if break_duration is not None:
            self.break_duration = break_duration
        self.mode = 'focus'
        self.duration = self.focus_duration
        self.remaining = self.duration
        self.is_running = False
        self.timer.stop()
        self.tick.emit(self.remaining)
