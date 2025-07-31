import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from welcome import WelcomePage
from dashboard import DashboardPage
from settings import SettingsPage

app = QApplication(sys.argv)

stack = QStackedWidget()

# First create dashboard and settings with None
dashboard = DashboardPage(stack, None)
settings = SettingsPage(stack, dashboard)
# Now link settings into dashboard
dashboard.settings_page = settings

welcome = WelcomePage(stack, dashboard, settings)

# Add to stack
stack.addWidget(welcome)
stack.addWidget(dashboard)
stack.addWidget(settings)

stack.setCurrentWidget(welcome)
stack.setBaseSize(400, 300)
stack.show()

sys.exit(app.exec_())
