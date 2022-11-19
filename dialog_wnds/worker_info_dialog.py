import sys
import datetime as dt
import dialog_wnds
from main import db_handlings as db_h

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMessageBox

from my_exceptions.my_exceptions import EmptyField, IntervalsIntersection, \
    IncorrectFormat, StartLatestThenEnd, EndAndEnteredDateBothEmpty

UI_FILENAME = 'properties/worker_info_dialog3.ui'
CALENDAR_ICON_FILENAME = 'properties/calendar_icon.png'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class WorkerInfoDialog(QDialog):
    def __init__(self, db, worker_id, fio='', was_empty=True):
        super(WorkerInfoDialog, self).__init__()
        self.was_empty = was_empty
        self.intervals = None
        self.worker_id = worker_id
        self.calendar_dialog = None
        self.fio = fio
        self.entered_date = ''
        self.start_date, self.end_date = '', ''
        self.profession = ''
        self.is_pedagogical = False
        self.table_content = []
        self.table_was_changed = False
        uic.loadUi(UI_FILENAME, self)
        self.set_table_params()
        if not self.was_empty:
            self.load_from_db(db)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Укажите сведения о сотруднике')
        self.set_btns_calendar_connections()
        self.set_btns_icon()
        self.ok_btn.setDefault(True)
        self.set_btns_connections()
        self.setWindowFlags(QtCore.Qt.WindowType.Window |
                            QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def load_from_db(self, db):
        self.fio, self.entered_date = db_h.get_one_worker(db,
                                                          self.worker_id)[0]
        self.intervals = db_h.get_worker_intervals(db, self.worker_id)
        self.fio_lineedit.setText(self.fio)
        self.entered_lineedit.setText(self.entered_date if
                                      self.entered_date != 'null' else '')
        self.table.setRowCount(0)
        for i, row in enumerate(self.intervals):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                if elem == 'null':
                    elem = ''
                item = QTableWidgetItem(elem if isinstance(elem, str)
                                        else ('да' if int(elem) else 'нет'))
                item.setBackground(QColor(240, 240, 240)
                                   if self.table.rowCount() % 2 == 0 else
                                   QColor('lightGray'))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled |
                              QtCore.Qt.ItemFlag.ItemIsSelectable)
                self.table.setItem(i, j, item)

    def set_btns_connections(self):
        self.add_row_btn.clicked.connect(self.add_row_to_table)
        self.remove_row_btn.clicked.connect(self.remove_row_from_table)
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn.clicked.connect(self.save_and_close)

    def set_btns_calendar_connections(self):
        self.calendar_btn_entered.clicked.connect(
            lambda: self.show_calendar_dialog(self.entered_lineedit))
        self.calendar_btn_start.clicked.connect(
            lambda: self.show_calendar_dialog(self.start_lineedit))
        self.calendar_btn_end.clicked.connect(
            lambda: self.show_calendar_dialog(self.end_lineedit))

    def set_table_params(self):
        self.table.setRowCount(0)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)

    def set_btns_icon(self):
        calendar_icon = QIcon(QPixmap(CALENDAR_ICON_FILENAME))
        self.calendar_btn_entered.setIcon(calendar_icon)
        self.calendar_btn_start.setIcon(calendar_icon)
        self.calendar_btn_end.setIcon(calendar_icon)

    def set_input_data_to_variables(self):
        self.fio = self.fio_lineedit.text()
        self.entered_date = self.entered_lineedit.text()
        self.start_date = self.start_lineedit.text()
        self.end_date = self.end_lineedit.text()
        self.profession = self.profession_lineedit.text()
        self.is_pedagogical = self.is_pedagogical_checkbox.isChecked()

    def add_row_to_table(self):
        self.set_input_data_to_variables()
        try:
            self.check_input_data(self.start_date, self.end_date,
                                  self.entered_date,
                                  self.profession, self.fio)
            self.table.setRowCount(self.table.rowCount() + 1)
            for i, elem in enumerate((self.start_date, self.end_date,
                                      self.profession, self.is_pedagogical)):
                if elem == '':
                    item = QTableWidgetItem('null')
                else:
                    item = QTableWidgetItem(elem if isinstance(elem, str)
                                            else str(int(elem)))
                item.setBackground(QColor(240, 240, 240)
                                   if self.table.rowCount() % 2 == 0 else
                                   QColor('lightGray'))
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled |
                              QtCore.Qt.ItemFlag.ItemIsSelectable)
                self.table.setItem(self.table.rowCount() - 1, i, item)
                self.table_was_changed = True
        except EmptyField as exception:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            field = '"Начало интервала"' if exception.where == 'start' else (
                '"Конец интервала"' if exception.where == 'end' else (
                    '"Должность"' if exception.where == 'prof' else '"ФИО"'))
            msg.setText(f'{exception.msg}: {field}')
            msg.exec_()
        except IncorrectFormat as exception:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            field = '"Начало интервала"' if exception.where == 'start' else (
                '"Конец интервала"' if exception.where == 'end' else
                '"Поступил в учреждение"')
            msg.setText(f'{exception.msg}: {field}')
            msg.exec_()
        except IntervalsIntersection:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Указанный интервал пересекается с уже существующим')
            msg.exec_()
        except ValueError as exception:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText(exception.args[0])
            msg.exec_()
        except StartLatestThenEnd:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Начало не может быть позже, чем конец')
            msg.exec_()
        except EndAndEnteredDateBothEmpty:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка')
            msg.setText('Конец интервала или дата поступления должен быть '
                        'указан')
            msg.exec_()
        self.ok_btn.setDefault(True)
        self.start_lineedit.setText('')
        self.end_lineedit.setText('')

    def check_input_data(self, start, end, entered, profession, fio):
        if not fio:
            raise EmptyField('Пустое поле', 'fio')
        if not start:
            raise EmptyField('Пустое поле', 'start')
        if not profession:
            raise EmptyField('Пустое поле', 'prof')

        if end == '' and entered == '':
            raise EndAndEnteredDateBothEmpty

        start_end_enter_list = [start]
        if entered:
            start_end_enter_list.append(entered)
        if end:
            start_end_enter_list.append(end)
        for _, elem in enumerate(start_end_enter_list):
            if len(elem.split('.')) != 3:
                raise IncorrectFormat('Неверный формат',
                                      'start' if _ == 0 else (
                                          'end' if _ == 1 else 'enter'))
            else:
                for i, j in enumerate(elem.split('.')):
                    if (i == 0 or i == 1) and len(j) != 2:
                        raise IncorrectFormat('Неверный формат',
                                              'start' if _ == 0 else (
                                                  'end' if _ == 1 else 'enter'
                                              ))
                    if i == 2 and len(j) != 4:
                        raise IncorrectFormat('Неверный формат',
                                              'start' if _ == 0 else (
                                                  'end' if _ == 1 else 'enter'
                                              ))

        self.table_content = [[self.table.item(i, j) for j in range(
            self.table.columnCount())] for i in range(self.table.rowCount())]
        intervals = []
        for i in self.table_content:
            start_date = i[0].text()
            end_date = i[1].text()
            d1, m1, y1 = map(int, start_date.split('.'))
            if end_date != 'null':
                d2, m2, y2 = map(int, end_date.split('.'))
                intervals.append((dt.date(y1, m1, d1), dt.date(y2, m2, d2)))
            else:
                intervals.append((dt.date(y1, m1, d1), 'null'))
        d_s, m_s, y_s = map(int, start.split('.'))
        if end:
            d_e, m_e, y_e = map(int, end.split('.'))
            end_check = dt.date(y_e, m_e, d_e)
        start_check = dt.date(y_s, m_s, d_s)
        if end:
            if start_check >= end_check:
                raise StartLatestThenEnd
        if entered:
            ent_day, ent_mon, ent_year = map(int, entered.split('.'))
            entered_date = dt.date(ent_year, ent_mon, ent_day)
        for j in intervals:
            if j[1] != 'null':
                if end:
                    if (j[0] <= start_check <= j[1]) or (
                            j[0] <= end_check <= j[1]):
                        raise IntervalsIntersection()
                else:
                    if j[0] <= start_check <= j[1]:
                        raise IntervalsIntersection
            else:
                if end:
                    if (j[0] <= start_check) or \
                            (j[0] <= end_check):
                        raise IntervalsIntersection
                else:
                    raise IntervalsIntersection

    def remove_row_from_table(self):
        rows = set()
        for i in self.table.selectedItems():
            rows.add(i.row())
        rows = tuple(rows)
        table_items = [[self.table.item(_, j).text() for j in range(
            self.table.columnCount())] for _ in range(
            self.table.rowCount()) if _ not in rows]
        for row in range(len(table_items)):
            color = QColor(240, 240, 240) if row % 2 == 1 else QColor(
                'lightGray')
            for column in range(len(table_items[row])):
                item = QTableWidgetItem(table_items[row][column])
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled |
                              QtCore.Qt.ItemFlag.ItemIsSelectable)
                item.setBackground(color)
                self.table.setItem(row, column, item)

        self.table.setRowCount(len(table_items))
        self.table_was_changed = True

    def show_calendar_dialog(self, line):
        if self.calendar_dialog is None:
            window = dialog_wnds.CalendarDialog()
            self.calendar_dialog = window
        else:
            window = self.calendar_dialog

        if window.exec_():
            date = window.calendarWidget.selectedDate()
            day, month = str(date.day()), str(date.month())
            year = str(date.year())
            day, month = map(lambda x: '0' + x if len(x) == 1 else x, (day,
                                                                       month))
            line.setText(f'{day}.{month}.{year}')

    def save_and_close(self):
        fio_changed = self.fio != self.fio_lineedit.text()
        if self.entered_lineedit.text() == '':
            if self.entered_date:
                entered_date_changed = self.entered_date != 'null'
            else:
                entered_date_changed = bool(self.entered_lineedit.text())
        else:
            entered_date_changed = self.entered_date != self.entered_lineedit.text()
        if self.table_was_changed or fio_changed or entered_date_changed:
            save_changes = QMessageBox.question(
                self, '', 'Сохранить изменения?', QMessageBox.Yes,
                QMessageBox.No)
            if save_changes == QMessageBox.Yes:
                self.table_content = [[self.table.item(i, j) for j in range(
                    self.table.columnCount())] for i in range(self.table.rowCount())]
                intervals = []
                for i in self.table_content:
                    start_date = i[0].text()
                    end_date = i[1].text()
                    d1, m1, y1 = map(int, start_date.split('.'))
                    if end_date != 'null':
                        d2, m2, y2 = map(int, end_date.split('.'))
                        intervals.append((dt.date(y1, m1, d1), dt.date(y2, m2, d2)))
                    else:
                        intervals.append((dt.date(y1, m1, d1), None))
                self.intervals = intervals
                self.fio = self.fio_lineedit.text()
                self.entered_date = self.entered_lineedit.text()
                self.entered_date = 'null' if not self.entered_date else self.entered_date
                self.accept()
            else:
                return
        else:
            self.reject()
