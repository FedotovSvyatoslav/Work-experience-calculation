import sys

from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, \
    QTableWidgetItem, QMenu, QFileDialog, QMessageBox

import dialog_wnds
from main import exp_calculate as exp_c
from main import db_handlings as db_h
from my_exceptions.my_exceptions import OpenException

MAINWINDOW_UI = 'properties/MainWindow5.ui'
MAINWIDGET_UI = 'properties/MainWidget.ui'
WINDOW_ICON_FILE = 'properties/staj_icon.ico'
CALENDAR_ICON_FILE = 'properties/calendar_icon.png'
PLUS_ICON_FILE = 'properties/plus_icon.png'
MINUS_ICON_FILE = 'properties/minus.png'


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def choose_day_correct_form(val):
    if 10 <= val <= 20:
        return 'дней'
    if val % 10 == 1:
        return 'день'
    if 2 <= (val % 10) <= 4:
        return 'дня'
    return 'дней'


def choose_month_correct_form(val):
    if 5 <= val <= 12 or val == 0:
        return 'месяцев'
    if val == 1:
        return 'месяц'
    return 'месяца'


def choose_year_correct_from(val):
    if 5 <= val <= 20:
        return 'лет'
    if val % 10 == 1:
        return 'год'
    if 2 <= (val % 10) <= 4:
        return 'года'
    return 'лет'


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.worker_info_dialog = None
        self.search_lineedit = None
        self.update_btn = None
        self.calendar_dialog = None
        self.db_name = None
        self.ask_file_wnd = None
        self.Table, self.add_row_btn, self.calendar_dialog_btn = None, None, None
        self.dateEdit = None
        self.remove_row_btn = None
        self.actionOpen, self.actionNew, self.actionSave = None, None, None
        self.empty_row_count = 0
        uic.loadUi(MAINWINDOW_UI, self)
        self.init_ui()

    def init_ui(self):
        self.set_window_params()

        self.fill_menubar()

        self.set_table_params()

        self.search_lineedit.textChanged.connect(lambda: self.update_table(
            'searching'))

        self.set_calendar_params()

        self.set_all_widget_enabled(False)

        self.add_row_btn.clicked.connect(self.add_row_in_table)
        self.remove_row_btn.clicked.connect(self.remove_row_from_table)
        self.set_icons_on_btns()

    def set_icons_on_btns(self):
        plus_icon = QIcon(QPixmap(PLUS_ICON_FILE))
        self.add_row_btn.setIcon(plus_icon)
        minus_icon = QIcon(QPixmap(MINUS_ICON_FILE))
        self.remove_row_btn.setIcon(minus_icon)

    def set_calendar_params(self):
        calendar_icon = QIcon(QPixmap(CALENDAR_ICON_FILE))
        self.calendar_dialog_btn.setIcon(calendar_icon)
        self.calendar_dialog_btn.clicked.connect(self.show_calendar_dialog)
        self.dateEdit.setDate(QDate(*exp_c.today()))
        self.update_btn.clicked.connect(lambda: self.update_table('date '
                                                                  'changed'))

    def set_window_params(self):
        self.setWindowTitle('Расчёт стажа')
        wnd_icon = QIcon(QPixmap(WINDOW_ICON_FILE))
        self.setWindowIcon(wnd_icon)
        self.setFixedSize(self.size())
        # Флаги, которые определяют это окно как Window, второй - убирает
        # изменение курсора, для изменения размера окна
        self.setWindowFlags(QtCore.Qt.WindowType.Window |
                            QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)

    def set_table_params(self):
        self.Table.setRowCount(1)
        self.Table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        self.Table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.Table.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        for i in range(self.Table.columnCount()):
            item = QTableWidgetItem('')
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.Table.setItem(0, i, item)
        self.Table.itemDoubleClicked.connect(self.elem_double_clicked)

    def fill_menubar(self):
        file_menu = QMenu(self)
        file_menu.setTitle('File')
        self.menuBar().addMenu(file_menu)

        open_action = QAction(self)
        open_action.setText('Open')
        open_action.triggered.connect(self.open_database)

        new_action = QAction(self)
        new_action.setText('New')
        new_action.triggered.connect(self.new_database)

        file_menu.addActions([open_action, new_action])

    def open_database(self, search_filter=None, db=None):
        self.set_all_widget_enabled(True)
        try_open_successfully = False
        if db is None:
            try:
                self.db_name = self.show_open_dialog()
                workers = db_h.get_workers(self.db_name)
                try_open_successfully = True
            except OpenException:
                try_open_successfully = False
        else:
            self.db_name = db
            try_open_successfully = True
            workers = db_h.get_workers(self.db_name)
        if try_open_successfully:
            self.Table.setRowCount(0)
            for i, worker in enumerate(workers):
                if search_filter:
                    if search_filter not in worker[1].lower():
                        continue
                color = self.choose_color(i)
                end_date = self.dateEdit.date()
                end_date = f'{end_date.day()}.{end_date.month()}.{end_date.year()}'
                if worker[1] or worker[2]:
                    worker_id = worker[0]
                    worker_entered_date = worker[2]
                    intervals = db_h.get_worker_intervals(self.db_name,
                                                          worker_id)
                    total_exp = exp_c.calc_total_exp(*[(_[0], _[1]) for _ in
                                                       intervals],
                                                     end2=end_date)
                    pedagogic_exp = exp_c.calc_total_exp(
                        *[(_[0], _[1]) for _ in
                          intervals if int(_[3])],
                        end2=end_date)
                    total_exp_before_entered = exp_c.calc_before_entering_exp(
                        worker[2], *[(_[0], _[1]) for _ in intervals],
                        end2=end_date)
                    pedagogic_exp_before_enter = exp_c.calc_before_entering_exp(
                        worker[2],
                        *[(_[0], _[1]) for _ in intervals if int(_[3])],
                        end2=end_date)
                    current_profession = db_h.get_current_profession(
                        self.db_name,
                        worker_id)
                else:
                    current_profession = ''
                    total_exp, total_exp_before_entered = '', ''
                    pedagogic_exp, pedagogic_exp_before_enter = '', ''
                    worker_id, worker_entered_date = '', ''
                self.Table.setRowCount(self.Table.rowCount() + 1)
                for j, elem in enumerate((
                        worker_id, worker[1], current_profession,
                        worker_entered_date, total_exp_before_entered,
                        pedagogic_exp_before_enter, total_exp,
                        pedagogic_exp)):
                    item = QTableWidgetItem()
                    if isinstance(elem, int) and (4 <= j <= 7):
                        years = int(elem) // 365
                        months = (int(elem) - (years * 365)) // 30
                        days = int(elem) - (years * 365) - (months * 30)
                        years_correct_form = choose_year_correct_from(years)
                        month_correct_form = choose_month_correct_form(months)
                        days_correct_form = choose_day_correct_form(days)
                        item.setText(f'{years} {years_correct_form}, '
                                     f'{months} {month_correct_form}, '
                                     f'{days} {days_correct_form}')
                    elif isinstance(elem, int) and j == 0:
                        item.setText(str(elem))
                    else:
                        if elem == 'null':
                            elem = ''
                        item.setText(elem)

                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled |
                                  QtCore.Qt.ItemFlag.ItemIsSelectable)
                    item.setBackground(color)
                    self.Table.setItem(self.Table.rowCount() - 1, j, item)

    def new_database(self):
        path = self.show_save_dialog()
        try:
            if not path:
                raise OpenException
            db_h.create_table_workers(path)
            db_h.create_table_intervals(path)
            self.open_database(db=path)
        except Exception:
            pass

    def add_row_in_table(self, was_update=False):
        self.Table.setRowCount(self.Table.rowCount() + 1)
        for i in range(self.Table.columnCount()):
            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled |
                          QtCore.Qt.ItemFlag.ItemIsSelectable)
            item.setBackground(self.choose_color(self.Table.rowCount() - 1))
            self.Table.setItem(self.Table.rowCount() - 1, i, item)
        if not was_update:
            self.empty_row_count = self.empty_row_count + 1

    def remove_row_from_table(self):
        rows = set()
        for i in self.Table.selectedItems():
            rows.add(i.row())
        rows = tuple(rows)
        any_row_contents_sth = False
        for i in rows:
            if any([self.Table.item(i, j).text() for j in range(
                    self.Table.columnCount())]):
                any_row_contents_sth = True
        if any_row_contents_sth:
            text_rows = [str(i + 1) for i in rows]
            sure = QMessageBox.question(self, '', 'Вы действительно хотите '
                                                  'удалить элементы с id ' +
                                        ', '.join(text_rows), QMessageBox.Yes,
                                        QMessageBox.No)
            if sure == QMessageBox.Yes:
                for i, row in enumerate(rows):
                    worker_id = int(self.Table.item(row - i, 0).text())
                    db_h.delete_one_worker(self.db_name, worker_id)
                    db_h.delete_worker_intervals(self.db_name, worker_id)
                    self.open_database(db=self.db_name)
                for i in range(self.empty_row_count):
                    self.add_row_in_table(was_update=True)
            else:
                return
        else:
            table_items = [[self.Table.item(_, j) for j in range(
                self.Table.columnCount())] for _ in range(
                self.Table.rowCount()) if _ not in rows]
            for row in range(len(table_items)):
                self.Table.setRowCount(self.Table.rowCount() + 1)
                for column in range(len(table_items[row])):
                    self.Table.setItem(row, column, table_items[row][column])
            self.Table.setRowCount(len(table_items))
            self.empty_row_count = self.empty_row_count - len(rows)

    def choose_color(self, i):
        color = QColor(240, 240, 240) if i % 2 == 1 else QColor(
            'lightGray')
        return color

    def elem_double_clicked(self, item):
        if item.column() != 1:
            return
        fio = item.text()
        entered_date = self.Table.item(item.row(), 3).text()
        is_empty = not (fio or entered_date)
        if not is_empty:
            worker_id = int(self.Table.item(item.row(), 0).text())
        else:
            worker_id = None
        dialog = dialog_wnds.WorkerInfoDialog(self.db_name, worker_id,
                                              fio=fio, was_empty=is_empty)

        if dialog.exec_():
            if dialog.was_empty:
                if dialog.fio or (dialog.entered_date != 'null'):
                    db_h.insert_worker(self.db_name, dialog.fio,
                                       dialog.worker_id, dialog.entered_date)
                    self.empty_row_count -= 1
            else:
                db_h.update_worker(self.db_name, dialog.worker_id, dialog.fio,
                                   dialog.entered_date)
                db_h.delete_worker_intervals(self.db_name, dialog.worker_id)
            for i in dialog.table_content:
                end_date = i[1].text()
                db_h.insert_one_worker_interval(
                    self.db_name, dialog.worker_id, i[0].text(), end_date,
                    i[2].text(), i[3].text(), None)
            self.update_table('elem updated')
            for i in range(self.empty_row_count):
                self.add_row_in_table(was_update=True)

    def update_table(self, why):
        if why == 'searching':
            str_to_search = self.search_lineedit.text().lower()
        else:
            str_to_search = None
        self.open_database(db=self.db_name, search_filter=str_to_search)

    def show_open_dialog(self):
        path = QFileDialog.getOpenFileName(self, 'Выберите базу данных',
                                           '', 'Sqlite database ('
                                               '*.sqlite)')[0]
        if not path:
            raise OpenException('')
        return path

    def show_save_dialog(self):
        path = QFileDialog.getSaveFileName(self, 'Сохранить базу данных как',
                                           '', 'Sqlite database ('
                                               '*.sqlite)')[0]
        return path

    def show_calendar_dialog(self):
        if self.calendar_dialog is None:
            window = dialog_wnds.CalendarDialog()
            self.calendar_dialog = window
        else:
            window = self.calendar_dialog

        if window.exec_():
            self.dateEdit.setDate(window.calendarWidget.selectedDate())

    def set_all_widget_enabled(self, is_enabled):
        self.add_row_btn.setEnabled(is_enabled)
        self.remove_row_btn.setEnabled(is_enabled)
        self.search_lineedit.setEnabled(is_enabled)
        self.update_btn.setEnabled(is_enabled)
        self.dateEdit.setEnabled(is_enabled)
        self.calendar_dialog_btn.setEnabled(is_enabled)
        self.Table.setEnabled(is_enabled)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
