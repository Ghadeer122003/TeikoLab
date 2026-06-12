import sqlite3

conn = sqlite3.connect('cell-count.db')
c = conn.cursor()

c.execute("""
    SELECT sa.sample_id, sa.b_cell, sa.cd8_t_cell, sa.cd4_t_cell, sa.nk_cell, sa.monocyte,
           su.response
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND su.response IN ('yes', 'no')
    AND sa.time_from_treatment_start = 0
""")

c.execute("""
    SELECT su.project, COUNT(*) as sample_count
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND sa.time_from_treatment_start = 0
    GROUP BY su.project
""")
print("Samples per project:", c.fetchall())

c.execute("""
    SELECT su.response, COUNT(DISTINCT sa.subject) as subject_count
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND sa.time_from_treatment_start = 0
    GROUP BY su.response
""")
print("Responders/Non-responders:", c.fetchall())

c.execute("""
    SELECT su.sex, COUNT(DISTINCT sa.subject) as subject_count
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND sa.time_from_treatment_start = 0
    GROUP BY su.sex
""")
print("Males/Females:", c.fetchall())

c.execute("""
    SELECT ROUND(AVG(sa.b_cell), 2)
    FROM samples sa
    JOIN subjects su ON sa.subject = su.subject
    WHERE su.condition = 'melanoma'
    AND su.treatment = 'miraclib'
    AND sa.sample_type = 'PBMC'
    AND sa.time_from_treatment_start = 0
    AND su.sex = 'M'
    AND su.response = 'yes'
""")
print("Avg b_cell melanoma male responders:", c.fetchone())