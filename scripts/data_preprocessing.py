import pandas as pd

# Load your actual dataset
df = pd.read_csv(r'C:\Users\shiva\Desktop\ER-Simulation-Analysis\data\er_wait_time.csv')

# Quick overview of data
print(df.head())
print(df.info())
print(df.isnull().sum())

# Convert 'Visit Date' to datetime
df['Visit Date'] = pd.to_datetime(df['Visit Date'])

# Feature Engineering (specific to your dataset)
# Total time metrics are already present as "Total Wait Time (min)"
# Creating more relevant metrics clearly

# Define total wait time clearly
df['Total_Wait_Time'] = df['Total Wait Time (min)']

# Define treatment-related times explicitly
df['Time_to_Registration'] = df['Time to Registration (min)']
df['Time_to_Triage'] = df['Time to Triage (min)']
df['Time_to_Medical_Professional'] = df['Time to Medical Professional (min)']

# Compute total processing time explicitly (registration + triage + medical professional)
df['Total_Processing_Time'] = (
    df['Time_to_Registration'] +
    df['Time_to_Triage'] +
    df['Time_to_Medical_Professional']
)

# Check if there's waiting after meeting medical professional
df['Additional_Wait'] = df['Total_Wait_Time'] - df['Total_Processing_Time']

# Extract hour and day of the week
df['Visit_Hour'] = df['Time of Day']
df['Day_of_Week'] = df['Day of Week']

# Save cleaned data
df.to_csv('C:/Users/shiva/Desktop/ER-Simulation-Analysis/data/cleaned_er_data.csv', index=False)

print("Data preprocessing completed successfully and saved to cleaned_er_data.csv.")
