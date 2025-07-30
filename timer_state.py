from PyQt5.QtCore import QObject, QTimer, pyqtSignal

class TimerState(QObject):
    tick = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.duration = 25 * 60
        self.remaining = self.duration
        self.is_running = False

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

    def _tick(self):
        self.remaining -= 1
        self.tick.emit(self.remaining)
        if self.remaining <= 0:
            self.stop()
            self.finished.emit()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)
    
    def stop(self):
        self.is_running = False
        self.timer.stop()

    def reset(self, duration=None):
        if duration:
            self.duration = duration
        self.remaining = self.duration
        self.stop()