from application.tetris_engine import TetrisEngine
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))  # Minimal window, not actually rendering
    pygame.display.set_caption("Key Event Listener")

    engine = TetrisEngine(rows=8, cols=4)
    engine.reset()
    engine.render()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Key 'W' pressed")
                elif event.key == pygame.K_a:
                    engine.perform_action(TetrisEngine.MOVE_LEFT)
                elif event.key == pygame.K_s:
                    engine.perform_action(TetrisEngine.DROP)
                    print("Key 'S' pressed")
                elif event.key == pygame.K_d:
                    engine.perform_action(TetrisEngine.MOVE_RIGHT)
                    print("Key 'D' pressed")
            engine.render()
    pygame.quit()

if __name__ == "__main__":
    main()
