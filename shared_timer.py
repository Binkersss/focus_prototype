from PyQt5.QtWidgets import QApplication
import sys

# Create QApplication if it doesn't exist
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

# Now it's safe to import and instantiate TimerState
from timer_state import TimerState
shared_timer = TimerState()
