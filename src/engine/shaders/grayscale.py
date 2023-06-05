from src.engine.shaders.abstract_shader import AbstractShader

import numpy as np

from numba import njit, prange
from typing import Tuple


@njit(fastmath=True, cache=True, parallel=True)
def compute_grayscale(input_array: np.ndarray,
                      weights: np.ndarray,
                      rect: np.ndarray,
                      output_array: np.ndarray) -> None:
    """0.5 ms for 600*500 surface, 0.13 ms for 400*300 surface"""

    size_x, size_y = input_array.shape[:2]
    start_x = max(rect[0], 0)
    end_x = min(rect[0] + rect[2], size_x)
    start_y = max(rect[1], 0)
    end_y = min(rect[1] + rect[3], size_y)

    r_map = np.empty(256, dtype='uint8')
    g_map = np.empty(256, dtype='uint8')
    b_map = np.empty(256, dtype='uint8')

    for k in range(256):
        r_map[k] = k * weights[0]
        g_map[k] = k * weights[1]
        b_map[k] = k * weights[2]

    for i in prange(start_x, end_x):
        for j in range(start_y, end_y):
            val = r_map[input_array[i, j, 0]] + \
                  g_map[input_array[i, j, 1]] + \
                  b_map[input_array[i, j, 2]]

            for channel in range(3):
                output_array[i, j, channel] = val


class GrayscaleShader(AbstractShader):
    INIT_VALUE = (0.3, 0.59, 0.11)
    FUNC = compute_grayscale

    @classmethod
    def shade(cls,
              input_surfarray,
              weights: Tuple[float, float, float] = None,
              rect = None,
              output_surfarray: np.ndarray = None) -> None:
        """
        Method used to grayscale a surface.

        Args:
            input_surfarray: A numpy array or a pygame surface that contain information to shade.
            weights: Weight of each color, sum must be equal to 1
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_surfarray: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        if weights is None:
            weights = (0.3, 0.59, 0.11)
        weights = np.array(weights)

        input_array, weights, rect_array, output_array = cls._adapt_args(input_surfarray=input_surfarray,
                                                                         values=weights,
                                                                         rect=rect,
                                                                         output_surfarray=output_surfarray)

        cls._compute(input_array=input_array,
                     values=weights,
                     rect_array=rect_array,
                     output_array=output_array)
