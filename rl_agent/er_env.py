import sys
import os

# Add the project root directory to sys.path to import 'scripts'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)


import gymnasium as gym
from gymnasium import spaces
import numpy as np
from scripts.simulation_backend import run_er_simulation

class EREnv(gym.Env):
    def __init__(self):
        super(EREnv, self).__init__()

        # Actions: Allocate doctors and nurses (each from 1 to 10)
        self.action_space = spaces.MultiDiscrete([10, 10])  # [doctors, nurses]

        # Observation: [Average Wait, Doctor Utilization, Nurse Utilization, Patients Treated]
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(4,), dtype=np.float32)

        # Static parameters
        self.arrival_rate = 10
        self.sim_time = 240

    def step(self, action):
        num_doctors, num_nurses = action + 1  # to ensure at least 1
        results = run_er_simulation(num_doctors, num_nurses, self.arrival_rate, self.sim_time)

        avg_wait = results['Average Wait Time (min)']
        doctor_util = results['Doctor Utilization (%)']
        nurse_util = results['Nurse Utilization (%)']
        patients_treated = results['Total Patients Treated']

        observation = np.array([avg_wait, doctor_util, nurse_util, patients_treated])

        # Reward: Negative avg wait time (the lower the wait, the higher the reward)
        reward = -avg_wait

        done = True  # Each episode is one simulation
        info = {}

        return observation, reward, done, False, info

    def reset(self, seed=None):
        observation = np.array([0.0, 0.0, 0.0, 0.0])
        return observation, {}
