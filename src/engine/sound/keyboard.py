import pygame

from src.engine.sound.instrument import Instrument, instru_list


class Keyboard:
    KEYS = {pygame.K_w: 0,
            pygame.K_s: 1,
            pygame.K_x: 2,
            pygame.K_d: 3,
            pygame.K_c: 4,
            pygame.K_v: 5,
            pygame.K_g: 6,
            pygame.K_b: 7,
            pygame.K_h: 8,
            pygame.K_n: 9,
            pygame.K_j: 10,
            pygame.K_COMMA: 11,

            pygame.K_a: 12,
            pygame.K_2: 13,
            pygame.K_z: 14,
            pygame.K_3: 15,
            pygame.K_e: 16,
            pygame.K_r: 17,
            pygame.K_5: 18,
            pygame.K_t: 19,
            pygame.K_6: 20,
            pygame.K_y: 21,
            pygame.K_7: 22,
            pygame.K_u: 23}

    CONFIG = {pygame.K_KP_0: 0,         # Select specific instrument
              pygame.K_KP_1: 1,
              pygame.K_KP_2: 2,
              pygame.K_KP_3: 3,
              pygame.K_KP_4: 4,
              pygame.K_KP_5: 5,
              pygame.K_KP_6: 6,
              pygame.K_KP_7: 7,
              pygame.K_KP_8: 8,
              pygame.K_KP_9: 9,

              pygame.K_KP_PLUS: 10,     # Octave += 1
              pygame.K_KP_MINUS: 11,    # Octave -= 1
              pygame.K_PAGEUP: 12,      # Next instrument
              pygame.K_PAGEDOWN: 13}    # Previous instrument

    current_octave_freq = 440
    current_octave = 3

    instruments = instru_list
    current_instrument = 0

    @classmethod
    def handle_inputs(cls, key):
        if key in cls.KEYS:
            return cls.play_sound(cls.KEYS[key])

        if key in cls.CONFIG:
            return cls.update_config(cls.CONFIG[key])

    @classmethod
    def update_config(cls, value):
        """
        0-9: Select instrument i
        10: Octave += 1
        11: Octave -= 1
        12: Next instrument
        13: Previous instrument
        """

        if 0 <= value < 10:
            cls.current_instrument = value
            return

        if value == 10:
            cls.current_octave_freq *= 2
            cls.current_octave += 1
            return

        if value == 11:
            cls.current_octave_freq /= 2
            cls.current_octave -= 1
            return

        if value == 12:
            cls.current_instrument = (cls.current_instrument + 1) % 10
            return

        if value == 13:
            cls.current_instrument = (cls.current_instrument - 1) % 10
            return

    @classmethod
    def play_sound(cls, note_pos):
        freq = cls.current_octave_freq * 2 ** (note_pos/12)
        cls.instruments[cls.current_instrument].play(1000, freq).play()
