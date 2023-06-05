import pygame

from src.engine.app import App
from src.engine.handlers.loop_handler import LoopHandler

from src.engine.sound.keyboard import Keyboard


def main():
    window = App.WINDOW

    while LoopHandler.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LoopHandler.quit_game()

            if event.type == pygame.KEYDOWN:
                Keyboard.handle_inputs(event.key)

                if event.key == pygame.K_ESCAPE:
                    LoopHandler.quit_game()

        # Computing
        pygame.display.set_caption(f"Instrument {Keyboard.instruments[Keyboard.current_instrument].name} | "
                                   f"Octave {Keyboard.current_octave}")

        # Rendering
        window.fill((255, 255, 255))

        pygame.display.flip()


if __name__ == '__main__':
    App.init("../../../assets")
    main()
