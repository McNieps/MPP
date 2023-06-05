import numpy.random
import pygame
import numpy as np
import scipy


class Synth:
    RATE = 44100
    DTYPE = "int16"
    FILTERS = {"lowpass": {}, "highpass": {}, "bandpass": {}, "bandstop": {}}

    @classmethod
    def init(cls):
        cls.saw(1000, 1000, 1)
        cls.sine(1000, 1000, 1)
        cls.square(1000, 1000, 1)

    @classmethod
    def create_pygame_sound(cls, wave):
        sound_array = np.empty((wave.shape[0], 2), dtype=cls.DTYPE)
        sound_array[:, 0] = wave
        sound_array[:, 1] = wave

        return pygame.sndarray.make_sound(sound_array)

    @classmethod
    def create_sound(cls, amplitude, frequency, duration, wave_function):
        samples = round(duration * cls.RATE)
        time_array = np.linspace(0, duration, samples)
        wave_array = amplitude * wave_function(time_array * 2 * np.pi * frequency)

        return wave_array

    @classmethod
    def empty(cls, duration):
        samples = round(duration * cls.RATE)
        return np.empty(samples)

    @classmethod
    def sine(cls, amplitude, frequency, duration):
        return cls.create_sound(amplitude, frequency, duration, np.sin)

    @classmethod
    def saw(cls, amplitude, frequency, duration):
        return cls.create_sound(amplitude, frequency, duration, scipy.signal.sawtooth)

    @classmethod
    def square(cls, amplitude, frequency, duration):
        return cls.create_sound(amplitude, frequency, duration, scipy.signal.square)

    @classmethod
    def noise(cls, amplitude, duration):
        samples = round(duration*cls.RATE)
        return numpy.random.randint(-amplitude, amplitude, samples)

    @classmethod
    def create_filter(cls, btype, order, frequency):
        """
        btype must be either lowpass, highpass, bandpass or bandstop
        order is the order of the filter
        frequency must be a scalar if lowpass or highpass, and must be a list of 2 scalars if bandpass or bandstop
        """

        if btype not in cls.FILTERS:
            raise Exception(f"{btype} is not a valid filter type. "
                            f"Please use either lowpass, highpass, bandpass or bandstop")

        if btype in ["bandpass", "bandstop"]:
            if type(frequency) not in [list, tuple] or len(frequency) != 2:
                raise Exception(f"Frequency must be a list/tuple of 2 scalar if btype={btype}")
            frequency = tuple(frequency)
            cutoff = [2*frequency[i]/cls.RATE for i in range(2)]

        else:
            if type(frequency) not in [float, int]:
                raise Exception(f"Frequency must be a scalar if btype={btype}")
            cutoff = 2*frequency/cls.RATE

        sos = scipy.signal.butter(order, cutoff, btype=btype, analog=True, output="sos")

        if order not in cls.FILTERS[btype]:
            cls.FILTERS[btype][order] = {}

        cls.FILTERS[btype][order][frequency] = sos

    @classmethod
    def get_filter(cls, btype, order, frequency):
        if btype in ["bandpass", "bandstop"]:
            frequency = tuple(frequency)

        if order not in cls.FILTERS[btype] or frequency not in cls.FILTERS[btype][order]:
            cls.create_filter(btype, order, frequency)

        return cls.FILTERS[btype][order][frequency]

    @classmethod
    def filter(cls, wave, btype, order, frequency):
        sos = cls.get_filter(btype, order, frequency)  # a, b = scipy.signal.butter(order, cutoff_frequency/nq, btype="low", analog=False)
        return scipy.signal.sosfiltfilt(sos, wave)

    @classmethod
    def fadeout(cls, duration):
        """Use exponential decay"""

        strength = duration / 5

        samples = round(duration * cls.RATE)
        time_array = np.linspace(0, duration, samples)
        wave_array = np.exp(-time_array/strength)

        return wave_array


Synth.init()
