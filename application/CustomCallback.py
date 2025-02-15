from stable_baselines3.common.callbacks import BaseCallback


# TODO: look if there is ok?
class CustomCallback(BaseCallback):
    def __init__(self, env, check_freq=8192, verbose=1):
        super(CustomCallback, self).__init__(verbose)
        self.env = env
        self.check_freq = check_freq
        self.step_counter = 0

    def _on_step(self) -> bool:
        self.step_counter += 1
        if self.step_counter % self.check_freq == 0:
            print(f"🔹 Custom event triggered at step {self.step_counter}")
            # Access the TetrisEnv or TetrisEngine instance here
            # 🔥 Correct way to access the original environment
            if hasattr(self.env, "env"):
                tetris_engine = self.env.env.engine  # Access the wrapped environment
            else:
                tetris_engine = self.env.engine  # Use directly if not wrapped

            # Append-adds at last
            file1 = open("deaths.cnt", "a")  # append mode
            file1.write(f"{str(tetris_engine.game_overs)}\n")
            file1.close()

            print(f"Total game overs in last {self.check_freq} Deaths: {tetris_engine.game_overs}")
            tetris_engine.game_overs = 0
            #print("Board State:\n", tetris_engine.get_board_state())
        return True
