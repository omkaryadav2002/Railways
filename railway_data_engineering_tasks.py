
# =========================
# Level 1: Data Exploration and Basic Operations
# =========================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import zipfile

# Load Data
df = pd.read_csv("Railway_info.csv")

# Task 1.1: Inspect Data
print(df.head(10))  # First 10 rows
print(df.info())    # Structure and data types
print(df.isnull().sum())  # Missing values

# Task 1.2: Basic Statistics
print("Number of Trains:", df['Train_No'].nunique())
print("Unique Source Stations:", df['Source_Station_Name'].nunique())
print("Unique Destination Stations:", df['Destination_Station_Name'].nunique())
print("Most Common Source Station:", df['Source_Station_Name'].value_counts().idxmax())
print("Most Common Destination Station:", df['Destination_Station_Name'].value_counts().idxmax())

# Task 1.3: Data Cleaning
df['Source_Station_Name'] = df['Source_Station_Name'].str.upper()
df['Destination_Station_Name'] = df['Destination_Station_Name'].str.upper()
df['days'] = df['days'].str.capitalize()

# =========================
# Level 2: Transformation and Aggregation
# =========================

# Task 2.1: Data Filtering
saturday_trains = df[df['days'] == 'Saturday']
specific_station = 'LUCKNOW JN.'
trains_from_specific = df[df['Source_Station_Name'] == specific_station]

# Task 2.2: Grouping and Aggregation
trains_per_source = df.groupby('Source_Station_Name').size().reset_index(name='Train_Count')
avg_trains_per_day = df.groupby(['Source_Station_Name', 'days']).size().groupby(level=0).mean().reset_index(name='Avg_Trains_Per_Day')

# Task 2.3: Data Enrichment
weekend = ['Saturday', 'Sunday']
df['Day_Type'] = df['days'].apply(lambda x: 'Weekend' if x in weekend else 'Weekday')

# =========================
# Level 3: Advanced Analysis
# =========================

# Task 3.1: Pattern Analysis
day_counts = df['days'].value_counts()
sns.barplot(x=day_counts.index, y=day_counts.values)
plt.title("Train Distribution by Days")
plt.xlabel("Days")
plt.ylabel("Train Count")
plt.tight_layout()
plt.savefig("trains_per_day.png")
plt.close()

# Task 3.2: Correlation and Insight
day_map = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
           'Friday': 5, 'Saturday': 6, 'Sunday': 7}
df['day_num'] = df['days'].map(day_map)
corr = df.groupby('day_num').size().reset_index(name='train_count')
correlation = corr['day_num'].corr(corr['train_count'])
print("Correlation between Day Number and Train Count:", round(correlation, 2))

# =========================
# Level 4: Visualization and Reporting
# =========================

output_dir = "railway_output"
os.makedirs(output_dir, exist_ok=True)

# Save visualizations
day_counts = df['days'].value_counts().reindex(day_map.keys())
plt.figure(figsize=(10, 5))
sns.barplot(x=day_counts.index, y=day_counts.values)
plt.title("Trains Per Day")
plt.xlabel("Day")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_dir}/trains_per_day.png")
plt.close()

# Top 10 Source Stations
top_sources = df['Source_Station_Name'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_sources.values, y=top_sources.index)
plt.title("Top 10 Source Stations")
plt.xlabel("Number of Trains")
plt.ylabel("Source Station")
plt.tight_layout()
plt.savefig(f"{output_dir}/top_sources.png")
plt.close()

# Top 10 Destination Stations
top_dest = df['Destination_Station_Name'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_dest.values, y=top_dest.index)
plt.title("Top 10 Destination Stations")
plt.xlabel("Number of Trains")
plt.ylabel("Destination Station")
plt.tight_layout()
plt.savefig(f"{output_dir}/top_destinations.png")
plt.close()

# Save top routes
routes = df.groupby(['Source_Station_Name', 'Destination_Station_Name']).size().reset_index(name='Count')
top_routes = routes.sort_values(by='Count', ascending=False).head(10)
top_routes.to_csv(f"{output_dir}/top_routes.csv", index=False)

# Summary Report
with open(f"{output_dir}/summary_report.txt", "w") as f:
    f.write("Train Data Analysis Report\n")
    f.write("==========================\n\n")
    f.write(f"Total Trains: {df['Train_No'].nunique()}\n")
    f.write(f"Unique Source Stations: {df['Source_Station_Name'].nunique()}\n")
    f.write(f"Unique Destination Stations: {df['Destination_Station_Name'].nunique()}\n\n")
    f.write(f"Most Common Source Station: {df['Source_Station_Name'].value_counts().idxmax()}\n")
    f.write(f"Most Common Destination Station: {df['Destination_Station_Name'].value_counts().idxmax()}\n\n")
    f.write(f"Correlation (Day Number vs Train Count): {round(correlation, 2)}\n")
    if correlation > 0.3:
        f.write("Insight: Positive trend – More trains toward weekend.\n")
    elif correlation < -0.3:
        f.write("Insight: Negative trend – Fewer trains toward weekend.\n")
    else:
        f.write("Insight: No strong trend across days.\n")

# ZIP packaging
with zipfile.ZipFile("railway_analysis_report.zip", "w") as zipf:
    for file in os.listdir(output_dir):
        zipf.write(os.path.join(output_dir, file), arcname=file)
