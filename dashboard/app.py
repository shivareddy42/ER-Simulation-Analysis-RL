import sys
import os

# Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

# Imports
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from stable_baselines3 import PPO          # <-- FIXED!
from rl_agent.er_env import EREnv
from scripts.simulation_backend import run_er_simulation

# Path to plots
plots_dir = os.path.join(current_dir, "..", "plots")

# -------------------------------
# Dashboard Title & Description
# -------------------------------
st.markdown("<h1 style='text-align: center; color: #2F4F4F;'>🚑 ER Operations Simulation Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
This interactive dashboard simulates Emergency Room operations based on real-world data.  
Adjust the parameters below and click **Run Simulation** to view results, including key metrics and dynamic visualizations.
""")

# -------------------------------
# Sidebar: RL Optimization
# -------------------------------
st.sidebar.header("RL Optimization")
use_rl = st.sidebar.checkbox("Use Reinforcement Learning for staff allocation?")

if use_rl:
    st.sidebar.info(
        "🔮 A pre-trained PPO agent dynamically suggests the optimal number of doctors and nurses "
        "to minimize patient wait times and maximize resource utilization."
    )
    agent = PPO.load("../rl_agent/trained_agent.zip")   # <-- FIXED: PPO.load
    env = EREnv()
    obs, _ = env.reset()
    action, _states = agent.predict(obs)
    num_doctors, num_nurses = action + 1  # ensure no 0 doctors/nurses
    st.sidebar.success(f"👨‍⚕️ RL Recommended Doctors: {num_doctors}")
    st.sidebar.success(f"👩‍⚕️ RL Recommended Nurses: {num_nurses}")

else:
    st.sidebar.header("Simulation Parameters (Manual)")
    num_doctors = st.sidebar.slider("Number of Doctors", 1, 10, 3, key="num_doctors_manual")
    num_nurses = st.sidebar.slider("Number of Nurses", 1, 10, 5, key="num_nurses_manual")

# Common parameters
arrival_rate = st.sidebar.slider("Patient Arrival Rate (patients per hour)", 1, 60, 10, key="arrival_rate_slider")
sim_duration = st.sidebar.slider("Simulation Duration (minutes)", 60, 480, 240, key="sim_duration_slider")

# -------------------------------
# Run Simulation Button
# -------------------------------
if st.sidebar.button("Run Simulation", key="run_simulation_button"):
    with st.spinner("Running multiple simulations, please wait..."):

        N_RUNS = 10
        all_results = []
        
        for _ in range(N_RUNS):
            result = run_er_simulation(num_doctors, num_nurses, arrival_rate, sim_time=sim_duration)
            all_results.append(result)

        # Average the key metrics
        avg_wait = np.mean([r['Average Wait Time (min)'] for r in all_results])
        patients_treated = np.mean([r['Total Patients Treated'] for r in all_results])
        doctor_utilization = np.mean([r['Doctor Utilization (%)'] for r in all_results])
        nurse_utilization = np.mean([r['Nurse Utilization (%)'] for r in all_results])

        # Pick wait times and queue lengths from the first run
        first_run = all_results[0]
        wait_times = first_run['All Wait Times']
        time_points = first_run['Time Points']
        queue_lengths = first_run['Queue Lengths']

    # Divider
    st.markdown("---")

    # -------------------------------
    # Display Key Metrics
    # -------------------------------
    st.subheader("Simulation Results (Key Metrics)")
    col1, col2 = st.columns(2)
    col1.metric("Average Wait Time (min)", f"{avg_wait:.2f}")
    col2.metric("Patients Treated", f"{patients_treated:.0f}")

    col3, col4 = st.columns(2)
    col3.metric("Doctor Utilization (%)", f"{doctor_utilization:.2f}")
    col4.metric("Nurse Utilization (%)", f"{nurse_utilization:.2f}")

    st.info("🧠 Metrics shown are averaged over multiple simulation runs to ensure stability and smoothness.")

    # Divider
    st.markdown("---")

    # -------------------------------
    # Plot 1: Patient Wait Time Distribution
    # -------------------------------
    st.subheader("Patient Wait Time Distribution")
    if wait_times:
        fig_hist = px.histogram(
            pd.DataFrame({'Wait Time (min)': wait_times}),
            x="Wait Time (min)",
            nbins=20,
            title="Histogram of Patient Wait Times",
            template="plotly_white"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.write("No wait time data available.")

    # Divider
    st.markdown("---")

    # -------------------------------
    # Plot 2: Queue Length Over Time
    # -------------------------------
    st.subheader("Queue Length Over Time")
    if time_points and queue_lengths:
        df_queue = pd.DataFrame({
            'Time (min)': time_points,
            'Total Queue Length': queue_lengths
        })
        fig_line = px.line(
            df_queue,
            x="Time (min)",
            y="Total Queue Length",
            title="ER Queue Length Over Simulation Time",
            markers=True,
            template="plotly_white"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.write("No queue data available.")

    # Divider
    st.markdown("---")

    # -------------------------------
    # Additional EDA Plots
    # -------------------------------
    with st.expander("📊 More EDA Plots"):
        st.markdown("These static plots provide additional insights into the ER dataset.")
        st.image(os.path.join(plots_dir, "avg_wait_time_by_hospital.png"), caption="Average Wait Time by Hospital", use_container_width=True)
        st.image(os.path.join(plots_dir, "avg_wait_time_by_urgency.png"), caption="Average Wait Time by Urgency Level", use_container_width=True)
        st.image(os.path.join(plots_dir, "correlation_heatmap.png"), caption="Correlation Heatmap", use_container_width=True)

# -------------------------------
# About Section (Always Visible)
# -------------------------------
with st.expander("ℹ️ About This Dashboard"):
    st.markdown("""
    **Overview:**  
    This interactive dashboard simulates Emergency Room (ER) operations using a discrete-event simulation model (SimPy).  
    Users can adjust parameters manually or leverage a Reinforcement Learning (RL) agent (PPO) to optimize staffing decisions.

    **Data Source:**  
    Cleaned real-world ER data from a Kaggle dataset.

    **Developed by:**  
    Shiva Reddy Peddireddy  
    **Inspired by:**  
    Dr. Vishnu Prabhu’s research on healthcare systems modeling and data-driven decision making.
    """)
