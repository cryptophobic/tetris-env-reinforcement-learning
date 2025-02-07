import sys

import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

from application.tetris_engine import CustomCallback
from application.tetris_env import TetrisEnv

try:
    # Create the environment
    env = TetrisEnv()

    envTimeLimit = gym.wrappers.TimeLimit(env, max_episode_steps=1000)

    # Define the RL model with logging
    # tensorboard_log_dir = "./ppo_tetris_log/"
    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=tensorboard_log_dir,
    #             learning_rate=0.00025, n_steps=4096, batch_size=64)
    model = PPO("MlpPolicy", envTimeLimit, verbose=1, learning_rate=0.00025, n_steps=2048, batch_size=64)

    # Train the model
    model.learn(total_timesteps=5000000, callback=CustomCallback(envTimeLimit, check_freq=2048))

    # Save the trained model
    model.save("tetris_ppo")

    # Evaluate the trained model
    # Create a separate evaluation environment wrapped with Monitor
    eval_env = Monitor(TetrisEnv())

    n_eval_episodes = 10
    episode_rewards = []

    for i in range(n_eval_episodes):
        print(f"Evaluating episode {i + 1}/{n_eval_episodes}...")
        episode_reward, _ = evaluate_policy(model, eval_env, n_eval_episodes=1, return_episode_rewards=True)
        episode_rewards.append(episode_reward[0])  # Extract reward from list
        print(f"Episode {i + 1} Reward: {episode_reward[0]}")

    mean_reward = sum(episode_rewards) / n_eval_episodes
    std_reward = (sum((r - mean_reward) ** 2 for r in episode_rewards) / n_eval_episodes) ** 0.5

    print(f"Final Mean Reward: {mean_reward}, Std Dev: {std_reward}")

    envTimeLimit.close()
except Exception as e:
    sys.stderr.write(str(e))
# Instructions to launch TensorBoard:
# Run the following command in the terminal:
# tensorboard --logdir=ppo_tetris_log/

# 3107
# 2339
# 1569
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#