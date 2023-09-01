import librosa
import numpy
import os
import math

from statistics import median
from scipy.signal import find_peaks
import matplotlib.pyplot as plot


class VoiceAnalyzer():
    """ Analyzes voice """

    def __init__(self, inputSamplesPaths: list[str]) -> None:
        self.__inputSamplesPaths = inputSamplesPaths

    def getFormants(self):
        for path in self.__inputSamplesPaths:
            print(f'\nFor file {path}:')
            sample, sr = librosa.load(path)

            spectrogram = numpy.abs(librosa.stft(sample))
            energy = numpy.sum(spectrogram, axis=1)
            peaks, _ = find_peaks(energy, threshold=10)

            formant_frequencies = librosa.fft_frequencies(sr=sr)[peaks]
            formant_frequencies = [f for f in formant_frequencies if f < 4500]

            energyFormants = {
                formant_frequencies[i]: energy[peaks[i]]
                for i in range(len(formant_frequencies))
            }

            sortedFormants = sorted(
                [
                    (k, v)
                    for k, v in energyFormants.items()
                ],
                key=lambda a: a[1],
                reverse=True
            )

            print('Top 3 formants by energy:')
            for f, e in sortedFormants[:3]:
                print('Formant', f, 'energy =', e)

            q = len(formant_frequencies) // 4

            # print(formant_frequencies)

            formants = []
            for i in range(4):
                max_energy = None
                max_f = None
                for f in formant_frequencies[q * i: q * (i + 1)]:
                    if max_f == None or energyFormants[f] > max_energy:
                        max_f = f
                        max_energy = energyFormants[f]
                formants.append(max_f)
                if len(formants) == 4:
                    break

            print('Min frequency:', formant_frequencies[0])
            print('Max frequency:', formant_frequencies[-1])
            for i in range(4):
                print(f'Formant {i + 1} =', formants[i])

            pitches = librosa.yin(
                y=sample,
                sr=sr,
                fmin=formant_frequencies[0],
                fmax=formants[3],
            )

            print('Fundamental frequency:', median(pitches))
