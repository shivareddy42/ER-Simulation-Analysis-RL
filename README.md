# 🚑 ER Operations Simulation Dashboard (with RL Optimization)

![ER Dashboard Banner](https://via.placeholder.com/1200x300?text=ER+Operations+Simulation+Dashboard)

---

## Overview

The **ER Operations Simulation Dashboard** is an interactive web app that models Emergency Room (ER) operations using a discrete-event simulation built with **SimPy**.

In this updated version, the dashboard also integrates a **Reinforcement Learning (RL)** agent (trained using **Proximal Policy Optimization (PPO)** from **Stable Baselines3**) to dynamically recommend optimal staff allocations (doctors and nurses) to minimize patient wait times and maximize resource utilization.

Users can either:
- **Manually adjust** staffing parameters, OR
- **Let the RL agent automatically recommend** the optimal number of doctors and nurses.

This project is inspired by the research of **Dr. Vishnu Prabhu** on healthcare systems modeling and decision making.

---

## Features

- ⚙️ **Interactive Manual Parameter Tuning**
- 🎯 **Reinforcement Learning Optimization with PPO**
- 📈 **Real-time SimPy-Based Simulation**
- 📊 **Dynamic Visualizations**
  - Histogram of Patient Wait Times
  - Queue Length Over Time
- 📚 **Additional EDA Plots**
- 🧠 **Metrics Averaged Over Multiple Runs for Stability**
- 🖥️ **Built with Streamlit + Plotly**

---

## Data Source

The simulation uses a cleaned version of real-world ER data from Kaggle.

**Dataset:** [ER Wait Time Dataset](https://www.kaggle.com/datasets/rivalytics/er-wait-time)

---

## Installation and Setup

1. **Clone this repository:**

   ```bash
   git clone https://github.com/shivareddy42/ER-Simulation-Analysis-RL.git
   cd ER-Simulation-Analysis-RL

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows


3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt


4. **Run the Streamlit app:**

   ```bash
   streamlit run dashboard/app.py

---

## Project Structure

ER-Simulation-Analysis-RL/
│
├── dashboard/
│   └── app.py
│
├── rl_agent/
│   ├── er_env.py
│   ├── trained_agent.zip
│
├── scripts/
│   └── simulation_backend.py
│
├── plots/
│   ├── avg_wait_time_by_hospital.png
│   ├── avg_wait_time_by_urgency.png
│   ├── correlation_heatmap.png
│
├── data/
│   └── cleaned_er_data.csv
│
├── requirements.txt
└── README.md


