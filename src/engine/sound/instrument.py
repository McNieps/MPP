from matplotlib import pyplot as plt

from src.engine.sound.synth import Synth


class Instrument:
    def __init__(self, name, duration=10):
        self.name = name
        self.duration = duration
        self.wave_function = basic

    def create_wave(self, amplitude, frequency):
        return self.wave_function(amplitude=amplitude, frequency=frequency, duration=self.duration)

    def play(self, amplitude, frequency):
        return Synth.create_pygame_sound(self.create_wave(amplitude, frequency))

    def show_waveform(self, amplitude, frequency):
        wave = self.create_wave(amplitude, frequency)
        plt.plot(wave)
        plt.show()


def basic(amplitude=1000, frequency=440, duration=2):
    fadeout = Synth.fadeout(duration)
    sine = Synth.sine(amplitude, frequency, duration)

    return sine * fadeout


def snare(amplitude=1000, frequency=440, duration=2):
    fadeout = Synth.fadeout(duration)
    noise = Synth.noise(amplitude, duration)

    return Synth.filter(fadeout*noise, "lowpass", 2, 100)


def noisy_test(amplitude=1000, frequency=440, duration=2):
    main_sine = Synth.sine(amplitude, frequency, duration)
    second_sine = Synth.sine(amplitude/10, frequency * 11, duration)

    return main_sine + second_sine


def filter_test(amplitude=1000, frequency=440, duration=2):
    base = noisy_test(amplitude, frequency, duration)
    return Synth.filter(base, "lowpass", 2, 40)


instru_list = [Instrument(chr(65+i)) for i in range(10)]
instru_list[0].name = "Basic"
instru_list[1].name, instru_list[1].wave_function, instru_list[1].duration = "Snare", snare, 0.5
instru_list[2].name, instru_list[2].wave_function, instru_list[2].duration = "NoisyTest", noisy_test, 1
instru_list[3].name, instru_list[3].wave_function, instru_list[3].duration = "FilterTest", filter_test, 1

if __name__ == '__main__':
    instru_list[2].show_waveform(1000, 40)
