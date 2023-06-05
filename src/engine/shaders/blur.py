from src.engine.shaders.abstract_shader import AbstractShader

import numpy as np

from numba import njit


@njit(fastmath=True, cache=True)
def compute_stack_blur(input_array: np.ndarray,
                       kernel_radius: int,
                       zone: np.ndarray,
                       output_array: np.ndarray) -> None:
    """
    1.2ms for 400*300 surface
    """

    size_x, size_y = input_array.shape[0], input_array.shape[1]
    start_x = max(0, min(zone[0], size_x))
    start_y = max(0, min(zone[1], size_y))
    end_x = max(0, min(zone[0] + zone[2], size_x))
    end_y = max(0, min(zone[1] + zone[3], size_y))

    max_x = size_x - 1
    max_y = size_y - 1

    kernel_size = 2 * kernel_radius + 1
    kernel_size_front = int((kernel_size - 1) / 2)
    kernel_size_back = int((kernel_size - 1) / 2) + 1

    # Intermediate array initialization
    intermediate_array = np.empty(input_array.shape, dtype='uint8')
    #     Top padding
    padding_min = max(start_y - kernel_radius, 0)
    intermediate_array[start_x: end_x, padding_min: start_y] = input_array[start_x: end_x, padding_min: start_y]
    #     Bottom padding
    padding_max = min(end_y + kernel_radius, size_y - 1)
    intermediate_array[start_x: end_x, end_y: padding_max] = input_array[start_x: end_x, end_y: padding_max]

    # Div map initialization
    div_map = np.zeros(256 * kernel_size, dtype='uint8')
    for k in range(256 * kernel_size):
        div_map[k] = k / kernel_size

    pixel_sum = np.empty(3, dtype='uint16')

    # Horizontal pass (Iterating over rows)
    for j in range(start_y, end_y):
        pixel_sum.fill(0)
        for i in range(start_x - 1 - kernel_radius, start_x + kernel_radius):
            i_adj = max(0, min(i, max_x))
            pixel_sum += input_array[i_adj, j]

        # Iterating over columns
        for i in range(start_x, end_x):
            i_add = min(i + kernel_size_front, max_x)
            i_rem = max(i - kernel_size_back, 0)
            for c in range(3):
                pixel_sum[c] = pixel_sum[c] \
                               + input_array[i_add, j, c] \
                               - input_array[i_rem, j, c]
                intermediate_array[i, j, c] = div_map[pixel_sum[c]]

    # Vertical pass (Iterating over columns)
    for i in range(start_x, end_x):
        pixel_sum.fill(0)
        for j in range(start_y - 1 - kernel_radius, start_y + kernel_radius):
            j_adj = max(0, min(j, max_y))
            pixel_sum += intermediate_array[i, j_adj]

        # Iterating over rows
        for j in range(start_y, end_y):
            j_add = min(j + kernel_size_front, max_y)
            j_rem = max(j - kernel_size_back, 0)
            for c in range(3):
                pixel_sum[c] = pixel_sum[c]\
                               + intermediate_array[i, j_add, c]\
                               - intermediate_array[i, j_rem, c]
                output_array[i, j, c] = div_map[pixel_sum[c]]


class BlurShader(AbstractShader):
    INIT_VALUE = 1
    FUNC = compute_stack_blur

    @classmethod
    def shade(cls,
              input_surfarray,
              kernel_radius: int,
              rect=None,
              output_surfarray=None) -> None:
        """
        Method used to blur a surface using stack-blur algorithm.

        Args:
            input_surfarray: A numpy array or a pygame surface that contain information to shade.
            kernel_radius: A int representing the kernel radius. The kernel size is equal to 2*kernel_radius+1
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_surfarray: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        input_array, values, rect_array, output_array = cls._adapt_args(input_surfarray,
                                                                        kernel_radius,
                                                                        rect,
                                                                        output_surfarray)

        cls._compute(input_array=input_array,
                     values=values,
                     rect_array=rect_array,
                     output_array=output_array)
