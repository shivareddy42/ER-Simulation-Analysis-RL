import os
import simpy
import numpy as np
import pandas as pd

def run_er_simulation(num_doctors, num_nurses, arrival_rate, sim_time=240):
    """
    Runs a discrete-event simulation of an emergency room.
    Returns key metrics and lists of wait times and queue lengths.
    """
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(script_dir, "..", "data")
    data_path = os.path.join(data_folder, "cleaned_er_data.csv")

    # Load data
    df = pd.read_csv(data_path)
    REGISTRATION_MEAN = df['Time_to_Registration'].mean()
    TRIAGE_MEAN = df['Time_to_Triage'].mean()
    MEDICAL_PRO_MEAN = df['Time_to_Medical_Professional'].mean()

    # Storage for results
    wait_times = []
    queue_lengths = []
    time_points = []
    resource_usage = {'doctor': 0, 'nurse': 0}

    # Define processes
    def patient(env, nurses, doctors):
        arrival = env.now
        with nurses.request() as req:
            yield req
            duration = np.random.exponential(REGISTRATION_MEAN)
            yield env.timeout(duration)
            resource_usage['nurse'] += duration
        with nurses.request() as req:
            yield req
            duration = np.random.exponential(TRIAGE_MEAN)
            yield env.timeout(duration)
            resource_usage['nurse'] += duration
        with doctors.request() as req:
            yield req
            duration = np.random.exponential(MEDICAL_PRO_MEAN)
            yield env.timeout(duration)
            resource_usage['doctor'] += duration
        wait_times.append(env.now - arrival)

    def generate_patients(env, nurses, doctors):
        while True:
            inter_arrival = np.random.exponential(60 / arrival_rate)
            yield env.timeout(inter_arrival)
            env.process(patient(env, nurses, doctors))

    def monitor(env, nurses, doctors):
        while True:
            total_queue = len(nurses.queue) + len(doctors.queue)
            time_points.append(env.now)
            queue_lengths.append(total_queue)
            yield env.timeout(5)

    # Set up environment
    env = simpy.Environment()
    nurses = simpy.Resource(env, capacity=num_nurses)
    doctors = simpy.Resource(env, capacity=num_doctors)
    env.process(generate_patients(env, nurses, doctors))
    env.process(monitor(env, nurses, doctors))

    env.run(until=sim_time)

    # Metrics
    avg_wait = np.mean(wait_times) if wait_times else 0
    throughput = len(wait_times)
    doctor_util = resource_usage['doctor'] / (sim_time * num_doctors) if sim_time and num_doctors else 0
    nurse_util = resource_usage['nurse'] / (sim_time * num_nurses) if sim_time and num_nurses else 0

    return {
        'Average Wait Time (min)': round(avg_wait, 2),
        'Total Patients Treated': throughput,
        'Doctor Utilization (%)': round(doctor_util * 100, 2),
        'Nurse Utilization (%)': round(nurse_util * 100, 2),
        'All Wait Times': wait_times,
        'Time Points': time_points,
        'Queue Lengths': queue_lengths
    }
