import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_SCRIPTS_DIR = os.path.join(BASE_DIR, "sql_scripts")

CREATE_TABLE_INTERVALS_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                               "create_table_intervals.sql")
CREATE_TABLE_WORKERS_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                             "create_table_workers.sql")
GET_WORKERS_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR, "select_workers.sql")
GET_WORKER_INTERVALS_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                             "select_worker_intervals.sql")
GET_ONE_WORKER_SQL_LITE = os.path.join(SQL_SCRIPTS_DIR,
                                       "select_one_worker.sql")
GET_CURRENT_PROFESSION_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                               "select_current_profession.sql")
INSERT_WORKER_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR, "insert_worker.sql")
INSERT_INTERVAL_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                        "insert_interval.sql")
DELETE_WORKER_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR, "delete_worker.sql")
DELETE_WORKER_INTERVALS_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                                "delete_worker_intervals.sql")
UPDATE_WORKER_NAME_SQL_FILE = os.path.join(SQL_SCRIPTS_DIR,
                                           "update_worker_name.sql")
UPDATE_WORKER_ENTERED_DATE_SQL_FILE = os.path.join(
    SQL_SCRIPTS_DIR, "update_worker_entered_date.sql")


def create_table_workers(db_name):
    """
    Создает таблицу workers в базе данных.

    Args:
        db_name (str): Имя файла базы данных SQLite.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(CREATE_TABLE_WORKERS_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read())
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {CREATE_TABLE_WORKERS_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while creating workers table: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def create_table_intervals(db_name):
    """
    Создает таблицу intervals в базе данных.

    Args:
        db_name (str): Имя файла базы данных SQLite.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(CREATE_TABLE_INTERVALS_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read())
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {CREATE_TABLE_INTERVALS_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while creating intervals table: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def get_workers(db_name):
    """
    Получает список всех работников из базы данных.

    Args:
        db_name (str): Имя файла базы данных SQLite.

    Returns:
        list: Список работников, отсортированных по ID.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(GET_WORKERS_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    result = db_cursor.execute(sql_file.read()).fetchall()
                return sorted(result, key=lambda x: x[0])
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {GET_WORKERS_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while getting workers: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def get_worker_intervals(db_name, worker_id):
    """
    Получает интервалы работы для конкретного работника.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.

    Returns:
        list: Список интервалов работы.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(GET_WORKER_INTERVALS_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    result = db_cursor.execute(sql_file.read(),
                                               (worker_id,)).fetchall()
                return result
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {GET_WORKER_INTERVALS_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while getting worker intervals: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def get_current_profession(db_name, worker_id):
    """
    Получает текущую профессию работника.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.

    Returns:
        str: Текущая профессия или пустая строка, если профессия не найдена.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(GET_CURRENT_PROFESSION_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    result = db_cursor.execute(sql_file.read(),
                                               (worker_id,)).fetchall()
                    return result[0][0] if result else ''
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {GET_CURRENT_PROFESSION_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while getting current profession: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def get_one_worker(db_name, worker_id):
    """
    Получает информацию об одном работнике.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.

    Returns:
        list: Информация о работнике.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(GET_ONE_WORKER_SQL_LITE,
                          'rt', encoding='utf-8') as sql_file:
                    result = db_cursor.execute(sql_file.read(),
                                               (worker_id,)).fetchall()
                return result
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {GET_ONE_WORKER_SQL_LITE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while getting one worker: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def insert_worker(db_name, worker_name, worker_id=None, entered=None):
    """
    Добавляет нового работника в базу данных.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_name (str): Имя работника.
        worker_id (int, optional): ID работника. Defaults to None.
        entered (str, optional): Дата приема на работу. Defaults to None.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(INSERT_WORKER_SQL_FILE,
                          'rt', encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read(),
                                      (worker_id, worker_name, entered))
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {INSERT_WORKER_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while inserting worker: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def insert_one_worker_interval(db_name, worker_id, start, end, profession,
                               is_profession_pedagogical, interval_id=None):
    """
    Добавляет интервал работы для работника.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.
        start (str): Дата начала интервала.
        end (str): Дата окончания интервала.
        profession (str): Название профессии.
        is_profession_pedagogical (bool): Является ли профессия педагогической.
        interval_id (int, optional): ID интервала. Defaults to None.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(INSERT_INTERVAL_SQL_FILE, 'rt',
                          encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read(),
                                      (interval_id, start, end,
                                       profession, is_profession_pedagogical,
                                       worker_id))
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {INSERT_INTERVAL_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while inserting interval: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def delete_one_worker(db_name, worker_id):
    """
    Удаляет работника из базы данных.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(DELETE_WORKER_SQL_FILE, 'rt',
                          encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read(), (worker_id,))
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {DELETE_WORKER_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while deleting worker: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def delete_worker_intervals(db_name, worker_id):
    """
    Удаляет все интервалы работы для работника.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(DELETE_WORKER_INTERVALS_SQL_FILE, 'rt',
                          encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read(), (worker_id,))
                db_connection.commit()
            except FileNotFoundError:
                raise FileNotFoundError(
                    f"SQL file not found: {DELETE_WORKER_INTERVALS_SQL_FILE}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while deleting worker intervals: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")


def update_worker(db_name, worker_id, new_name, new_date):
    """
    Обновляет информацию о работнике.

    Args:
        db_name (str): Имя файла базы данных SQLite.
        worker_id (int): ID работника.
        new_name (str): Новое имя работника.
        new_date (str): Новая дата приема на работу.

    Raises:
        FileNotFoundError: Если SQL-файл не найден.
        sqlite3.Error: Если произошла ошибка базы данных.
    """
    try:
        with sqlite3.connect(db_name) as db_connection:
            db_cursor = db_connection.cursor()
            try:
                with open(UPDATE_WORKER_NAME_SQL_FILE, 'rt',
                          encoding='utf-8') as sql_file:
                    db_cursor.execute(sql_file.read(), (new_name, worker_id))
                with open(UPDATE_WORKER_ENTERED_DATE_SQL_FILE, 'rt',
                          encoding='utf-8') as sql_file2:
                    db_cursor.execute(sql_file2.read(), (new_date, worker_id))
                db_connection.commit()
            except FileNotFoundError as e:
                raise FileNotFoundError(f"SQL file not found: {e}")
            except sqlite3.Error as e:
                raise sqlite3.Error(
                    f"Database error while updating worker: {e}")
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to connect to database: {e}")
