import sqlite3

CREATE_TABLE_INTERVALS_SQL_FILE = 'sql_scripts/create_table_intervals.sql'
CREATE_TABLE_WORKERS_SQL_FILE = 'sql_scripts/create_table_workers.sql'

GET_WORKERS_SQL_FILE = 'sql_scripts/select_workers.sql'
GET_WORKER_INTERVALS_SQL_FILE = 'sql_scripts/select_worker_intervals.sql'
GET_ONE_WORKER_SQL_LITE = 'sql_scripts/select_one_worker.sql'
GET_CURRENT_PROFESSION_SQL_FILE = 'sql_scripts/select_current_profession.sql'

INSERT_WORKER_SQL_FILE = 'sql_scripts/insert_worker.sql'
INSERT_INTERVAL_SQL_FILE = 'sql_scripts/insert_interval.sql'

DELETE_WORKER_SQL_FILE = 'sql_scripts/delete_worker.sql'
DELETE_WORKER_INTERVALS_SQL_FILE = 'sql_scripts/delete_worker_intervals.sql'

UPDATE_WORKER_NAME_SQL_FILE = 'sql_scripts/update_worker_name.sql'
UPDATE_WORKER_ENTERED_DATE_SQL_FILE = 'sql_scripts/update_worker_entered_date.sql'


def create_table_workers(db_name):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(CREATE_TABLE_WORKERS_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read())
    db_connection.commit()


def create_table_intervals(db_name):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(CREATE_TABLE_INTERVALS_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read())
    db_connection.commit()


def get_workers(db_name):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(GET_WORKERS_SQL_FILE, 'rt') as sql_file:
        result = db_cursor.execute(sql_file.read()).fetchall()
    return sorted(result, key=lambda x: x[0])


def get_worker_intervals(db_name, worker_id):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(GET_WORKER_INTERVALS_SQL_FILE, 'rt') as sql_file:
        result = db_cursor.execute(sql_file.read(), (worker_id,)).fetchall()
    return result


def get_current_profession(db_name, worker_id):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(GET_CURRENT_PROFESSION_SQL_FILE, 'rt') as sql_file:
        result = db_cursor.execute(sql_file.read(), (worker_id, )).fetchall()
    if not result:
        return ''
    return result[0][0]


def get_one_worker(db_name, worker_id):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(GET_ONE_WORKER_SQL_LITE, 'rt') as sql_file:
        result = db_cursor.execute(sql_file.read(), (worker_id,)).fetchall()
    return result


def insert_worker(db_name, worker_name, worker_id=None, entered=None):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    row_count = len(get_workers(db_name))
    with open(INSERT_WORKER_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (worker_id, worker_name,
                                            entered))
    db_connection.commit()


def insert_one_worker_interval(db_name, worker_id, start, end, profession,
                               is_profession_pedagogical, interval_id=None):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(INSERT_INTERVAL_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (interval_id, start, end,
                                            profession,
                                            is_profession_pedagogical,
                                            worker_id))
    db_connection.commit()


def delete_one_worker(db_name, worker_id):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(DELETE_WORKER_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (worker_id, ))
    db_connection.commit()


def delete_worker_intervals(db_name, worker_id):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(DELETE_WORKER_INTERVALS_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (worker_id,)).fetchall()
    db_connection.commit()


def update_worker(db_name, worker_id, new_name, new_date):
    db_connection = sqlite3.connect(db_name)
    db_cursor = db_connection.cursor()
    with open(UPDATE_WORKER_NAME_SQL_FILE, 'rt') as sql_file:
        db_cursor.execute(sql_file.read(), (new_name, worker_id)).fetchall()
    with open(UPDATE_WORKER_ENTERED_DATE_SQL_FILE, 'rt') as sql_file2:
        db_cursor.execute(sql_file2.read(), (new_date, worker_id)).fetchall()
    db_connection.commit()