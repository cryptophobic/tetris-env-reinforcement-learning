from time import sleep

import pygame

from application.Engine import Engine
from application.Perform import Action
from application.config import DESK_HEIGHT, DESK_WIDTH


def main():

    engine = Engine(rows=DESK_HEIGHT, cols=DESK_WIDTH, render_type="Graphics")
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
                elif event.key == pygame.K_a:
                    engine.action(Action.MOVE_LEFT)
                elif event.key == pygame.K_s:
                    engine.action(Action.DROP)
                elif event.key == pygame.K_d:
                    engine.action(Action.MOVE_RIGHT)
            engine.render()


    engine.tracker.flush_to_disk()
    pygame.quit()

if __name__ == "__main__":
    main()
