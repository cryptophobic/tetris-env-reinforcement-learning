import gymnasium as gym
from gymnasium import spaces
import numpy as np
from application.tetris_engine import TetrisEngine


class TetrisEnv(gym.Env):
    """
    Custom Gymnasium environment for a simplified single-player Tetris game
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self):
        super(TetrisEnv, self).__init__()

        # Initialize Tetris engine
        self.engine = TetrisEngine()

        # Define action space (0: left, 1: right, 2: rotate, 3: down, 4: drop)
        self.action_space = spaces.Discrete(5)

        # Define observation space (20x10 board with binary values)
        self.observation_space = spaces.Box(low=0, high=1, shape=(20, 10), dtype=np.float32)

    def reset(self):
        """Reset the game to start a new episode"""
        self.engine.reset()
        return self._get_state(), {}

    def step(self, action):
        """Perform an action in the game"""
        self.engine.perform_action(action)

        # Get new state and reward
        state = self._get_state()
        reward = self.engine.get_reward()
        done = self.engine.is_game_over()

        return state, reward, done, False, {}

    def _get_state(self):
        """Extract the current board state as an observation"""
        return self.engine.get_board_state()

    def render(self, mode='human'):
        """Render the game (optional for visualization)"""
        self.engine.render()

    def close(self):
        """Cleanup if needed"""
        pass
