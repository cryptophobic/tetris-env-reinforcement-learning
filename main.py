from time import sleep

from application.Engine import Engine
import pygame

from application.Perform import Action


def main():
    pygame.init()
    screen = pygame.display.set_mode((1, 1))  # Minimal window, not actually rendering
    pygame.display.set_caption("Key Event Listener")

    engine = Engine(rows=10, cols=10)
    engine.reset()
    engine.render()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    engine.action(Action.ROTATE)
                    print("Key 'W' pressed")
                elif event.key == pygame.K_a:
                    engine.action(Action.MOVE_LEFT)
                elif event.key == pygame.K_s:
                    engine.action(Action.DROP)
                    print("Key 'S' pressed")
                elif event.key == pygame.K_d:
                    engine.action(Action.MOVE_RIGHT)
                    print("Key 'D' pressed")
            engine.render()


    engine.tracker.flush_to_disk()
    pygame.quit()

if __name__ == "__main__":
    main()
