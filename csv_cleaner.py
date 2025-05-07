import pandas as pd

df = pd.read_csv('raw_game_logs/RED SOX_3-8-2025_Stats.csv', header=1)

# Trimming columns to keep and dumping those that we are not using
columns_to_keep = ["Number", "Last", "First", "GP", "PA", "AB", "AVG", "OBP", "OPS", "SLG", "H", "1B", "2B", "3B", "HR", "RBI", "R", "BB", "SO", "HBP", "BB/K", "BABIP", "SF"]
df = df[columns_to_keep]

# Combine duplicate players stats
for col in df.columns[3:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
combined = df.groupby([df.columns[0], df.columns[1], df.columns[2]], as_index=False).sum()

# Recalculating stats that are based on other columns
combined['AVG'] = round(combined['H'] / combined['AB'], 3)
combined['OBP'] = round((combined['H'] + combined['BB'] + combined['HBP']) / (combined['AB'] + combined['BB'] + combined['HBP'] + combined['SF']), 3)
combined['SLG'] = round((combined['1B'] + combined['2B'] * 2 + combined['3B'] * 3 + combined['HR'] * 4) / combined['AB'], 3)
combined['OPS'] = round(combined['OBP'] + combined['SLG'], 3)
combined['BB/K'] = round(combined['BB'] / combined['SO'], 3)
combined['BABIP'] = round((combined['H'] - combined['HR']) / (combined['AB'] - combined['HR'] - combined['SO'] + combined['SF']), 3)

combined.to_csv("clean_game_logs/red_sox_3-8_stats_clean.csv", index = False)