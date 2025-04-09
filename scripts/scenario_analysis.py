import matplotlib.pyplot as plt

scenarios = ['Baseline (5 Nurses, 3 Doctors)', 'Improved (7 Nurses, 5 Doctors)']
avg_wait_times = [359.93, 171.48]  # replace these with your actual simulated averages clearly

plt.figure(figsize=(12,6))
plt.bar(scenarios, avg_wait_times, color=['crimson', 'mediumseagreen'])
plt.title('Average Patient Wait Times: Baseline vs Improved Resources')
plt.ylabel('Average Wait Time (minutes)')
plt.grid(axis='y')
plt.savefig('C:/Users/shiva/Desktop/ER-Simulation-Analysis/plots/scenario_comparison.png')
plt.close()
