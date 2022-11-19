from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

UI_FILENAME = 'properties/calendar_dialog.ui'


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