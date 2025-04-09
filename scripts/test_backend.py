from simulation_backend import run_er_simulation

results = run_er_simulation(num_doctors=3, num_nurses=5, arrival_rate=10)
print(results)
