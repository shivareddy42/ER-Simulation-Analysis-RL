import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir))
sys.path.append(project_root)

from stable_baselines3 import PPO
from rl_agent.er_env import EREnv

# Create the environment
env = EREnv()

# Create the PPO agent
model = PPO("MlpPolicy", env, verbose=1)

# Train the agent
print("Starting training...")
model.learn(total_timesteps=10000)  # You can increase this for better results
print("Training complete!")

# Save the trained agent
save_path = os.path.join(current_dir, "rl_agent", "trained_agent")
model.save(save_path)

print(f"Agent saved at {save_path}.zip")
