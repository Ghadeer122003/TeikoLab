import sqlite3
import csv

conn = sqlite3.connect('cell-count.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS subjects (
    project TEXT,
    subject TEXT PRIMARY KEY,
    condition TEXT,
    sex TEXT,
    age INTEGER,
    treatment TEXT,
    response TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS samples (
    sample_id TEXT PRIMARY KEY,
    subject TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER,
    b_cell INTEGER,
    cd8_t_cell INTEGER,
    cd4_t_cell INTEGER,
    nk_cell INTEGER,
    monocyte INTEGER,
    FOREIGN KEY (subject) REFERENCES subjects(subject)
)""")


def process_csv(conn, cur, filename):
    with open (filename, "rt") as f:
        reader = csv.reader(f)
        next(reader, None)
        for entry in reader: 
            try: 
                print(reader.line_num)
                cur.execute("INSERT OR IGNORE INTO subjects (project, subject, condition, sex, age, treatment, response) VALUES (?,?,?,?,?,?,?)",
                            (entry[0], entry[1], entry[2], entry[4], entry[3], entry[5], entry[6]))
                cur.execute("INSERT OR IGNORE INTO samples (sample_id, subject, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte) VALUES (?,?,?,?,?,?,?,?,?)",
                            (entry[7], entry[1], entry[8], entry[9], entry[10], entry[11], entry[12], entry[13], entry[14]))
            except Exception as e: 
                print(e)

process_csv(conn, c, 'cell-count.csv')
conn.commit()
conn.close()