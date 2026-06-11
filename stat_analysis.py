import matplotlib.pyplot as plt
from scipy import stats
import sqlite3
import pandas as pd
import seaborn as sns


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
""")

def compare_differences(rows):
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    responders = {p: [] for p in populations}
    non_responders = {p: [] for p in populations}

    
    for row in rows:
        sample_id = row[0]
        counts = [row[1], row[2], row[3], row[4], row[5]]
        response = row[6]
        total = sum(counts)
        
        for i, pop in enumerate(populations):
            pct = (counts[i] / total) * 100
            if response == 'yes':
                responders[pop].append(pct)
            else:
                non_responders[pop].append(pct)
    
    # stats test
    for pop in populations:
        stat, p_value = stats.mannwhitneyu(responders[pop], non_responders[pop])
        significant = "SIGNIFICANT" if p_value < 0.05 else "not significant"
        print(f"{pop}: p={p_value:.4f} -> {significant}")
    
    return responders, non_responders

rows = c.fetchall()
responders, non_responders = compare_differences(rows)
conn.close()

#BoxPlots
def plot_boxplot(responders, non_responders):
    populations = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
    
    # build a flat list of records
    data = []
    for pop in populations:
        for val in responders[pop]:
            data.append({'population': pop, 'percentage': val, 'response': 'responder'})
        for val in non_responders[pop]:
            data.append({'population': pop, 'percentage': val, 'response': 'non_responder'})
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='population', y='percentage', hue='response')
    plt.title('Cell Population Frequencies: Responders vs Non-Responders')
    plt.savefig('boxplot.png')
    plt.show()

plot_boxplot(responders, non_responders)



