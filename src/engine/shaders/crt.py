import numpy as np

from numba import njit, prange


@njit(fastmath=True, cache=True, parallel=True)
def compute_crt(input_array: np.ndarray,
                strength: float,
                zone: np.ndarray,
                output_array: np.ndarray) -> None:

    output_array = np.zeros(input_array.shape, "uint8")

    size_x, size_y = input_array.shape[:2]
    max_i, max_j = size_x-1, size_y-1

    # Creating offset-ed uv_map
    uv_map = np.empty((size_x, size_y, 2))
    for i in range(size_x):
        for j in range(size_y):
            uv_map[i, j] = 0.5-i/max_i, 0.5-j/max_j

    # Mapping
    for i in prange(size_x):
        for j in range(size_y):
            ni = int(min(1, max(0, i/max_i+uv_map[i, j, 1]**2*uv_map[i, j, 0] * strength))*max_i)
            nj = int(min(1, max(0, j/max_j+uv_map[i, j, 0]**2*uv_map[i, j, 1] * strength))*max_j)

            output_array[ni][nj] = input_array[i, j]

    input_array[:] = output_array[:]


class CRT:
    @classmethod
    def compute(cls,
                input_array,
                strength,
                rect,
                output_array):
        """
        Method used to distort the surface, making it crt style

        Args:
            input_array:
            strength:
            rect:
            output_array:
        """
        compute_crt(input_array, 0.25, np.zeros(5), np.zeros(5))
        del input_array

        compute_crt(np.zeros((10, 10, 3), "uint8"), 0.25, np.zeros(5), np.zeros(5))


