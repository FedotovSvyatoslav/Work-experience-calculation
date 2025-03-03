import os

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_FILENAME = os.path.join(CURRENT_DIR, "..", "..", "resources",
                           "calendar_dialog.ui")


class CalendarDialog(QDialog):
    def __init__(self):
        super(CalendarDialog, self).__init__()
        self.calendarWidget = None
        uic.loadUi(UI_FILENAME, self)
        self.init_ui()
        self.result = self.calendarWidget.selectedDate()

    def init_ui(self):
        self.ok_btn.setDefault(True)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)