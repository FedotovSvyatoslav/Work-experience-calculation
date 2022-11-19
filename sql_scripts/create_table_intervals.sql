CREATE TABLE exp_intervals (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    start_i        TEXT,
    end_i          TEXT,
    profession     TEXT,
    is_pedagogical INTEGER,
    worker_id              REFERENCES workers (id)
);
