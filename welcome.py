from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class WelcomePage(QWidget):
    def __init__(self, stack, dashboard_page, settings_page):
        super().__init__()
        self.stack = stack
        self.dashboard_page = dashboard_page
        self.settings_page = settings_page

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Focus Drift"))
        layout.addWidget(QLabel("Focus better. Work smarter."))

        start_btn = QPushButton("Start")
        start_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        layout.addWidget(start_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_page))
        layout.addWidget(settings_btn)

        self.setLayout(layout)
