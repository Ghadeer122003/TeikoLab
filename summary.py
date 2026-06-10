import sqlite3

conn = sqlite3.connect('cell-count.db')
c = conn.cursor()

def get_frequency_summary(cur):
    cur.execute("SELECT * FROM samples")
    rows = cur.fetchall()
    
    summary = []
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    for row in rows:
        sample_id = row[0]
        counts = [row[4], row[5], row[6], row[7], row[8]]
        total_count = sum(counts)
        
        for i, population in enumerate(populations):
            percentage = (counts[i] / total_count) * 100
            summary.append({
                'sample': sample_id,
                'total_count': total_count,
                'population': population,
                'count': counts[i],
                'percentage': round(percentage, 2)
            })
    
    return summary

results = get_frequency_summary(c)
for row in results:
    print(row)

conn.close()