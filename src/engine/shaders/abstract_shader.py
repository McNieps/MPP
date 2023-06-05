import pygame
import numpy as np

from typing import Any


def abstract_shade_function(input_array: np.ndarray,
                            values: Any,
                            rect_array: np.ndarray,
                            output_array: np.ndarray) -> None:
    print(input_array)
    print(values)
    print(rect_array)
    print(output_array)


class AbstractShader:
    WINDOW_SIZE = (400, 300)
    SHADER_MAX_SIZE = 100
    INITIALIZED = False
    INIT_VALUE = 0
    FUNC = abstract_shade_function

    @classmethod
    def shade(cls,
              input_surfarray,
              values: Any,
              rect,
              output_surfarray):
        """
        Args:
            input_surfarray: A numpy array or a pygame surface that contain information to shade.
            values: A argument that may change from one shader to another. No defined type.
            rect: A rect style argument that describe the zone to shade. Default to the whole array.
            output_surfarray: A numpy array or a pygame surface that will receive the shaded array.
                Default to the input_array.
        """

        input_array, values, rect_array, output_array = cls._adapt_args(input_surfarray=input_surfarray,
                                                                        values=values,
                                                                        rect=rect,
                                                                        output_surfarray=output_surfarray)

        cls._compute(input_array=input_array,
                     values=values,
                     rect_array=rect_array,
                     output_array=output_array)

    @classmethod
    def _compute(cls,
                 input_array: np.ndarray,
                 values: Any,
                 rect_array: np.ndarray,
                 output_array: np.ndarray) -> None:
        """
        Args:
            input_array: A numpy array that contain information to shade.
            values: An argument that may change from one shader to another. No defined type.
            rect_array: A numpy array argument that describe the zone to shade.
            output_array: A numpy array that will receive the shaded array.
        """

        cls.FUNC(input_array, values, rect_array, output_array)

        if not cls.INITIALIZED:
            cls._initialize()

    @classmethod
    def _adapt_args(cls,
                    input_surfarray,
                    values: Any,
                    rect=None,
                    output_surfarray=None) -> tuple[np.ndarray, Any, np.ndarray, np.ndarray]:

        # input_array definition
        if isinstance(input_surfarray, pygame.Surface):
            input_array = pygame.surfarray.pixels3d(input_surfarray)
        elif isinstance(input_surfarray, np.ndarray):
            input_array = input_surfarray
        else:
            raise TypeError(f"{type(input_surfarray)} is not a valid surfarray type.")

        # output_array definition
        if output_surfarray is input_surfarray or output_surfarray is None:
            output_array = input_array
        elif isinstance(output_surfarray, pygame.Surface):
            output_array = pygame.surfarray.pixels3d(output_surfarray)
        elif isinstance(output_surfarray, np.ndarray):
            output_array = output_surfarray
        else:
            raise TypeError(f"{type(output_surfarray)} is not a valid surfarray type.")

        # rect_array definition
        if rect is None:
            rect_array = np.array((0, 0, *input_array.shape[:2]), dtype="uint16")
        elif isinstance(rect, (list, tuple, pygame.Rect)):
            rect_array = np.array(rect, dtype="uint16")
        else:
            raise TypeError(f"{rect} is not a valid rect argument.")

        # verifications
        if input_array.shape != output_array.shape:
            raise ValueError(f"The size of the input {input_array.shape} and "
                             f"the size of the output {output_array.shape} does not match.")

        return input_array, values, rect_array, output_array

    @classmethod
    def _initialize(cls):
        cls.INITIALIZED = True

        input_array = np.zeros((10, 10, 3), dtype="uint8")
        values = cls.INIT_VALUE
        rect_array = np.array((0, 0, 10, 10), dtype="uint16")
        output_array = input_array

        cls._compute(input_array=input_array,
                     values=values,
                     rect_array=rect_array,
                     output_array=output_array)
