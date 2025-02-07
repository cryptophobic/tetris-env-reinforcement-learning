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
        self.engine = TetrisEngine(rows=4, cols=4)

        # Define action space (0: left, 1: right, 2: rotate, 3: down, 4: drop)
        self.action_space = spaces.Discrete(3)
        self.action_counter = 0  # Track how many actions have been taken
        # Define observation space (20x10 board with binary values)
        self.observation_space = spaces.Box(low=0, high=1, shape=(self.engine.rows, self.engine.cols), dtype=np.float32)

    def reset(self, seed=None, options=None):
        """Reset the game state"""
        if seed is not None:
            np.random.seed(seed)  # Ensure deterministic resets

        #self.engine.current_reward = 0
        """Reset the game to start a new episode"""
        self.engine.reset()
        return self._get_state(), {}

    def step(self, action):
        """Perform an action in the game"""
        self.engine.perform_action(action)
        self.action_counter += 1

        # Force the piece to move down every 10 actions
        if self.action_counter % 5 == 0:
            self.engine.fall()  # 3 corresponds to "move down"

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
        print("Closing environment")
        """Cleanup if needed"""
        pass
