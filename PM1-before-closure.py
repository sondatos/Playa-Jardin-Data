import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])  # Chart takes 4/5 of space, stats take 1/5


# Data for PM1
data_pm1 = {
    "Fecha Toma": [
        "01/07/2024", "17/06/2024", "04/06/2024", "03/06/2024", "20/05/2024", "06/05/2024",
        "22/04/2024", "18/03/2024", "05/03/2024", "19/02/2024", "05/02/2024", "22/01/2024",
        "20/11/2023", "24/10/2023", "23/10/2023", "16/10/2023", "25/09/2023", "11/09/2023",
        "28/08/2023", "07/08/2023", "24/07/2023", "10/07/2023", "19/06/2023", "05/06/2023",
        "22/05/2023", "08/05/2023", "24/04/2023", "10/04/2023", "27/03/2023", "06/03/2023",
        "27/02/2023", "13/02/2023", "23/01/2023", "14/11/2022", "17/10/2022", "03/10/2022",
        "27/09/2022", "13/09/2022", "30/08/2022", "09/08/2022", "19/07/2022", "04/07/2022",
        "22/06/2022", "07/06/2022", "24/05/2022", "10/05/2022", "26/04/2022", "05/04/2022",
        "21/03/2022", "08/03/2022", "15/02/2022", "08/02/2022", "18/01/2022", "16/11/2021",
        "09/11/2021", "19/10/2021", "05/10/2021", "28/09/2021", "14/09/2021", "31/08/2021",
        "09/08/2021", "26/07/2021", "06/07/2021", "24/06/2021", "08/06/2021", "24/05/2021",
        "10/05/2021", "27/04/2021", "05/04/2021", "22/03/2021", "10/03/2021", "09/03/2021",
        "16/02/2021", "08/02/2021", "18/01/2021"
    ],
    "Escherichia coli": [
        390, 3, 5, 360, 13, 3, 90, 180, 30, 350, 90, 200, 280, 290, 380, 110, 120, 3, 9, 170,
        50, 130, 40, 100, 3, 3, 6, 16, 9, 160, 120, 280, 70, 260, 150, 110, 160, 150, 180, 170,
        220, 110, 10, 80, 9, 10, 100, 9, 30, 9, 40, 40, 20, 160, 60, 70, 60, 9, 20, 20, 80, 10,
        9, 30, 9, 40, 30, 80, 9, 270, 9, 10, 40, None, None
    ],
    "Enterococo": [
        170, 3, 7, 30, 11, 40, 25, 50, 15, 90, 30, 40, 80, 70, 40, 50, 48, 4, 12, 29, 32, 24, 4,
        18, 6, 5, 1, 5, 10, 31, 29, 70, 19, 42, 21, 10, 37, 44, 40, 46, 50, 30, 3, 10, 3, 3, 46,
        5, 14, 9, 5, 14, 8, 37, 12, 33, 10, 6, 5, 7, 21, 3, 5, 3, 3, 17, 4, 13, 5, 3, 50, 3, 4, 5
    ]
}

# Ensure all lists are the same length
max_length = max(len(data_pm1[key]) for key in data_pm1)
for key in data_pm1:
    while len(data_pm1[key]) < max_length:
        data_pm1[key].append(None)

# Convert to DataFrame
df_pm1 = pd.DataFrame(data_pm1)
df_pm1['Fecha Toma'] = pd.to_datetime(df_pm1['Fecha Toma'], format='%d/%m/%Y')

# Handle duplicates by taking the maximum value for each date
df_pm1 = df_pm1.groupby('Fecha Toma').max().reset_index()

# Group by month and compute maximum values
df_pm1_monthly = df_pm1.resample('M', on='Fecha Toma').max().reset_index()

# Calculate statistics for the monthly data
stats = df_pm1_monthly[['Escherichia coli', 'Enterococo']].agg(['mean', 'median', 'min', 'max', 'std'])

# Plotting the bar chart for PM1 with statistics annotations
ax1 = plt.subplot(gs[0])
ax1.bar(df_pm1_monthly['Fecha Toma'] - pd.Timedelta(days=7), df_pm1_monthly['Escherichia coli'], width=15, label='Escherichia coli (UFC/100 mL)', alpha=0.7)
ax1.bar(df_pm1_monthly['Fecha Toma'] + pd.Timedelta(days=7), df_pm1_monthly['Enterococo'], width=15, label='Enterococo (UFC/100 mL)', alpha=0.7)
ax1.set_xlabel('Date')
ax1.set_ylabel('Values (UFC/100 mL)')
ax1.set_title('Playa Jardin PM1 - Charcón Derecha')
ax1.legend(loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_xticks(df_pm1_monthly['Fecha Toma'])
ax1.set_xticklabels(df_pm1_monthly['Fecha Toma'].dt.strftime('%b %Y'), rotation=45)

# Statistics section
ax2 = plt.subplot(gs[1])
ax2.axis('off')  # Turn off the axes for the stats section
stat_text = '\n'.join([f"{key.capitalize()}: {stats.loc[key].to_dict()}" for key in stats.index])
ax2.text(0.5, 0.5, stat_text, fontsize=10, horizontalalignment='center', verticalalignment='center', bbox=dict(boxstyle="round", alpha=0.5))

plt.tight_layout()
plt.show()

# Print statistics for reference
print("Statistics for Monthly Data:")
print(stats)