import numpy
import librosa
import matplotlib.pyplot as plot
import soundfile as sf

from scipy import signal

class AudioProcessor():
    def __init__(self, inputPath: str, outputPath: str) -> None:
        self.__inputPath = inputPath
        self.__outputPath = outputPath
    
    def wave(self):
        sample, sr = librosa.load(self.__inputPath)

        fig, ax = plot.subplots(nrows=1)
        librosa.display.waveshow(sample, sr=sr, ax=ax)
        ax.set(title='Waveform')
        ax.label_outer()
        plot.savefig(f"{self.__outputPath}/waveplot.png")
        plot.clf()

    def stft(self, windows: list, seconds: int):
        """ Short-Time Fourier Transform """

        sample, sr = librosa.load(self.__inputPath)
        
        n_fft = int(seconds * sr)
        ms = int(seconds * 1000)

        for window in windows:
            S = numpy.abs(
                librosa.stft(sample, window=window, n_fft=n_fft)
            )

            fig, ax = plot.subplots()

            img = librosa.display.specshow(
                librosa.amplitude_to_db(S),
                y_axis='log',
                x_axis='time',
                ax=ax,
            )

            name = window.__name__

            ax.set_title(f"{name} window spectrogram [{ms}ms]")
            fig.colorbar(img, ax=ax, format="%+2.0f dB")

            plot.savefig(f"{self.__outputPath}/{name}_{ms}.png")
            plot.clf()

    def noiseFilter(self, seconds: int):
        sample, sr = librosa.load(self.__inputPath)
        n_fft = int(seconds * sr)
        ms = int(seconds * 1000)
        
        sample = signal.wiener(sample)

        S = numpy.abs(librosa.stft(sample, n_fft=n_fft))

        fig, ax = plot.subplots()

        img = librosa.display.specshow(
            librosa.amplitude_to_db(S),
            y_axis='log',
            x_axis='time',
            ax=ax,
        )

        ax.set_title(f"filtered spectrogram [{ms}ms]")
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

        plot.savefig(f"{self.__outputPath}/filtered_{ms}.png")
        plot.clf()

        sf.write(
            f"{self.__outputPath}/filtered.wav", 
            sample, 
            sr, 
            subtype='PCM_24'
        )
