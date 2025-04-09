import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data for realistic distributions
df = pd.read_csv('C:/Users/shiva/Desktop/ER-Simulation-Analysis/data/cleaned_er_data.csv')

# Parameters derived from data
INTER_ARRIVAL_MEAN = df['Total_Wait_Time'].mean()
REGISTRATION_MEAN = df['Time_to_Registration'].mean()
TRIAGE_MEAN = df['Time_to_Triage'].mean()
MEDICAL_PRO_MEAN = df['Time_to_Medical_Professional'].mean()

# Define simulation parameters
SIM_TIME = 24*60  # simulate 24 hours
NUM_NURSES = 5
NUM_DOCTORS = 3

# Data collection lists
wait_times = []

# Patient arrival process
def patient(env, patient_id, nurses, doctors):
    arrival_time = env.now

    # Registration process (handled by nurses)
    with nurses.request() as req:
        yield req
        registration_duration = np.random.exponential(REGISTRATION_MEAN)
        yield env.timeout(registration_duration)

    # Triage process (also by nurses)
    with nurses.request() as req:
        yield req
        triage_duration = np.random.exponential(TRIAGE_MEAN)
        yield env.timeout(triage_duration)

    # Medical professional consultation (doctors)
    with doctors.request() as req:
        yield req
        consultation_duration = np.random.exponential(MEDICAL_PRO_MEAN)
        yield env.timeout(consultation_duration)

    total_wait = env.now - arrival_time
    wait_times.append(total_wait)

# Patient generator based on real arrival rates
def patient_generator(env, nurses, doctors):
    patient_id = 0
    while True:
        inter_arrival_time = np.random.exponential(INTER_ARRIVAL_MEAN/10) # Adjusted for realism
        yield env.timeout(inter_arrival_time)
        patient_id += 1
        env.process(patient(env, patient_id, nurses, doctors))

# Setup and run simulation
env = simpy.Environment()
nurses = simpy.Resource(env, capacity=NUM_NURSES)
doctors = simpy.Resource(env, capacity=NUM_DOCTORS)
env.process(patient_generator(env, nurses, doctors))

# Run the simulation
env.run(until=SIM_TIME)

# Visualization: Wait time distribution after simulation
plt.figure(figsize=(12,6))
plt.hist(wait_times, bins=30, color='teal', alpha=0.7)
plt.title('Simulated Patient Wait Times over 24 hours')
plt.xlabel('Wait time (minutes)')
plt.ylabel('Number of patients')
plt.grid(True)
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/simulated_wait_times.png')
plt.close()

# Output average wait time clearly
print(f"Average simulated patient wait time: {np.mean(wait_times):.2f} minutes")
