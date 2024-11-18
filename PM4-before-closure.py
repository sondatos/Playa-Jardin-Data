import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Create a figure with two sections: one for the bar chart and one for the statistics
fig = plt.figure(figsize=(12, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1])  # Chart takes 4/5 of space, stats take 1/5


# Data setup
data = {
    "Fecha Toma": [
        "01/07/2024", "17/06/2024", "03/06/2024", "20/05/2024", "06/05/2024", "22/04/2024",
        "08/04/2024", "18/03/2024", "05/03/2024", "19/02/2024", "05/02/2024", "22/01/2024",
        "20/11/2023", "23/10/2023", "16/10/2023", "25/09/2023", "11/09/2023", "28/08/2023",
        "07/08/2023", "24/07/2023", "10/07/2023", "19/06/2023", "05/06/2023", "22/05/2023",
        "08/05/2023", "24/04/2023", "10/04/2023", "27/03/2023", "06/03/2023", "27/02/2023",
        "13/02/2023", "23/01/2023", "14/11/2022", "17/10/2022", "03/10/2022", "27/09/2022",
        "14/09/2022", "13/09/2022", "01/09/2022", "30/08/2022", "16/08/2022", "20/07/2022",
        "19/07/2022", "04/07/2022", "22/06/2022", "07/06/2022", "24/05/2022", "10/05/2022",
        "26/04/2022", "05/04/2022", "21/03/2022", "08/03/2022", "17/02/2022", "15/02/2022",
        "08/02/2022", "18/01/2022", "16/11/2021", "09/11/2021", "19/10/2021", "05/10/2021",
        "28/09/2021", "14/09/2021", "31/08/2021", "09/08/2021", "26/07/2021", "06/07/2021",
        "24/06/2021", "22/06/2021", "08/06/2021", "24/05/2021", "24/05/2021", "17/05/2021",
        "27/04/2021", "05/04/2021", "22/03/2021", "09/03/2021", "16/02/2021", "08/02/2021",
        "18/01/2021"
    ],
    "Escherichia coli": [
        70, 40, 580, 801, 60, 190, 40, 220, 40, 80, 140, 160, 410, 570, 280, 600, 210, 250,
        250, 280, 170, 40, 130, 130, 290, 290, 140, 30, 200, 440, 500, 180, 360, 80, 400, 630,
        20, 280, 150, 290, 230, 30, 270, 220, 40, 70, 9, 80, 320, 60, 30, 40, 150, 320, 70,
        70, 190, 230, 90, 170, 10, 10, 20, 230, 30, 30, 50, None, 230, 10, 9, 290, 50, 60, 30,
        220, 10, 30, 20
    ],
    "Enterococo": [
        50, 22, 100, 290, 27, 100, 19, 55, 14, 45, 72, 90, 260, 60, 90, 160, 100, 190, 48, 100,
        110, 29, 50, 40, 55, 3, 25, 22, 45, 90, 160, 20, 140, 25, 44, 100, 81, 170, 29, 110,
        95, 3, 80, 60, 7, 21, 3, 16, 40, 8, 3, 12, 15, 80, 20, 23, 80, 54, 32, 80, 7, 3, 10, 40,
        7, 20, 4, None, 63, 3, 3, 7, 17, 29, 1, 75, 9, 30, 4
    ]
}

# Create DataFrame
df = pd.DataFrame(data)
df['Fecha Toma'] = pd.to_datetime(df['Fecha Toma'], format='%d/%m/%Y')

# Group by month and compute maximum values
df_monthly = df.resample('M', on='Fecha Toma').max().reset_index()

# Calculate statistics
stats = df_monthly[['Escherichia coli', 'Enterococo']].agg(['mean', 'median', 'min', 'max', 'std'])

# Plotting the bar chart
ax1 = plt.subplot(gs[0])
ax1.bar(df_monthly['Fecha Toma'] - pd.Timedelta(days=7), df_monthly['Escherichia coli'], width=15, label='Escherichia coli (UFC/100 mL)', alpha=0.7)
ax1.bar(df_monthly['Fecha Toma'] + pd.Timedelta(days=7), df_monthly['Enterococo'], width=15, label='Enterococo (UFC/100 mL)', alpha=0.7)
ax1.set_xlabel('Date')
ax1.set_ylabel('Values (UFC/100 mL)')
ax1.set_title('Playa Jardin PM4 Playa Grande')
ax1.legend(loc='upper left')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_xticks(df_monthly['Fecha Toma'])
ax1.set_xticklabels(df_monthly['Fecha Toma'].dt.strftime('%b %Y'), rotation=45)

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