import numpy as np

from src.engine.shaders.abstract_shader import AbstractShader


def compute_chromatic_aberration(input_array: np.ndarray,
                                 rgb_dx_dy: tuple[tuple[int, int],
                                                  tuple[int, int],
                                                  tuple[int, int]],
                                 rect: np.ndarray,
                                 output_array: np.ndarray) -> None:

    size_x, size_y = input_array.shape[0:2]
    start_x = max(rect[0], 0)
    end_x = min(rect[0]+rect[2], size_x)
    start_y = max(rect[1], 0)
    end_y = min(rect[1]+rect[3], size_y)

    for c in range(3):
        if rgb_dx_dy[c]:
            output_array[start_x:end_x, start_y:end_y, c] = np.roll(input_array[start_x:end_x, start_y:end_y, c],
                                                                    rgb_dx_dy[c],
                                                                    (0, 1))


class ChromaticAberrationShader(AbstractShader):
    INIT_VALUE = ((0, 0), (0, 0), (0, 0))
    FUNC = compute_chromatic_aberration

    @classmethod
    def shade(cls,
              input_surfarray,
              rgb_dx_dy: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
              rect=None,
              output_surfarray=None) -> None:
        """
        Method used to blur a spread R, G and B color channels.

        Args:
            input_surfarray: A numpy array or a pygame surface that contain information to shade.
            rgb_dx_dy: Offset of each color layer
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_surfarray: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        input_array, rgb_dx_dy, rect_array, output_array = cls._adapt_args(input_surfarray=input_surfarray,
                                                                           values=rgb_dx_dy,
                                                                           rect=rect,
                                                                           output_surfarray=output_surfarray)

        cls._compute(input_array=input_array,
                     values=rgb_dx_dy,
                     rect_array=rect_array,
                     output_array=output_array)
