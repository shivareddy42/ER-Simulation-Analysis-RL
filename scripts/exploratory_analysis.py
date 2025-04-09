import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned dataset
df = pd.read_csv('C:/Users/shiva/Desktop/ER-Simulation-Analysis/data/cleaned_er_data.csv')

# Visualization 1: Patient Visits by Hour of the Day
plt.figure(figsize=(12, 6))
sns.countplot(x='Visit_Hour', data=df, palette='viridis')
plt.title('Patient Visits by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Number of Visits')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/patient_visits_by_hour.png')
plt.close()

# Visualization 2: Patient Visits by Day of Week
plt.figure(figsize=(12, 6))
sns.countplot(x='Day_of_Week', data=df, palette='Set2', 
              order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title('Patient Visits by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Visits')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/patient_visits_by_day.png')
plt.close()

# Visualization 3: Distribution of Total Wait Time
plt.figure(figsize=(12, 6))
sns.histplot(df['Total_Wait_Time'], kde=True, bins=30, color='purple')
plt.title('Distribution of Total Wait Time (min)')
plt.xlabel('Total Wait Time (minutes)')
plt.ylabel('Frequency')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/total_wait_time_distribution.png')
plt.close()

# Visualization 4: Average Wait Time by Hospital
plt.figure(figsize=(12, 6))
sns.barplot(x='Hospital Name', y='Total_Wait_Time', data=df, palette='coolwarm', ci=None)
plt.title('Average Wait Time by Hospital')
plt.xlabel('Hospital')
plt.ylabel('Average Wait Time (minutes)')
plt.xticks(rotation=10)
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/avg_wait_time_by_hospital.png')
plt.close()

# Visualization 5: Average Wait Time by Urgency Level
plt.figure(figsize=(12, 6))
sns.barplot(x='Urgency Level', y='Total_Wait_Time', data=df, palette='magma', ci=None)
plt.title('Average Wait Time by Urgency Level')
plt.xlabel('Urgency Level')
plt.ylabel('Average Wait Time (minutes)')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/avg_wait_time_by_urgency.png')
plt.close()

# Visualization 6: Correlation Heatmap (Key numerical columns)
plt.figure(figsize=(12, 8))
numeric_cols = [
    'Nurse-to-Patient Ratio', 'Specialist Availability', 'Facility Size (Beds)',
    'Time_to_Registration', 'Time_to_Triage', 'Time_to_Medical_Professional',
    'Total_Wait_Time', 'Total_Processing_Time', 'Additional_Wait', 'Patient Satisfaction'
]
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap of Key Variables')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/correlation_heatmap.png')
plt.close()

print("EDA complete, all plots saved successfully.")
