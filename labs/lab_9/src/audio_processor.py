import numpy
import librosa
import matplotlib.pyplot as plot
import soundfile as sf
import os

from scipy import signal


class AudioProcessor():
    def __loadSamplesPaths(self, supportAudioExts: list[str]):
        samplesData = []
        for ext in supportAudioExts:
            for file in os.listdir(self.__inputFolderPath):
                if file.endswith(f".{ext}"):
                    samplesData.append(f"{self.__inputFolderPath}/{file}")
        return samplesData

    def __init__(
        self,
        inputFolderPath: str,
        outputPath: str,
        supportAudioExts=['wav'],
    ) -> None:
        self.__inputFolderPath = inputFolderPath
        self.__outputPath = outputPath
        self.samplesPaths = self.__loadSamplesPaths(
            supportAudioExts=supportAudioExts,
        )

    def wave(self):
        for path in self.samplesPaths:
            sample, sr = librosa.load(path)

            filename, ext = os.path.basename(path).split('.')

            fig, ax = plot.subplots(nrows=1)
            librosa.display.waveshow(sample, sr=sr, ax=ax)
            ax.set(title='Waveform')
            ax.label_outer()
            plot.savefig(f"{self.__outputPath}/{filename}_waveplot.png")
            plot.clf()

    @staticmethod
    def plot(sample, n_fft, title: str, outputFilePath: str, yAxisMode='log'):
        S = numpy.abs(librosa.stft(sample, n_fft=n_fft))
        fig, ax = plot.subplots()

        img = librosa.display.specshow(
            librosa.amplitude_to_db(S, ref=numpy.max),
            y_axis=yAxisMode,
            x_axis='time',
            ax=ax,
        )

        pitches = librosa.yin(
            sample,
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7')
        )  

        print(n_fft)
        times = librosa.times_like(pitches, hop_length=950)

        ax.set_title(title)
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

        ax.plot(times, pitches, label='f0', color='cyan', linewidth=2)
        ax.legend(loc='upper right')

        plot.savefig(outputFilePath)
        plot.close()

    def stft(self, windows: list, seconds: int, yAxisMode="log"):
        """ Short-Time Fourier Transform """

        for path in self.samplesPaths:
            sample, sr = librosa.load(path)

            n_fft = int(seconds * sr)
            ms = int(seconds * 1000)

            for window in windows:
                name = window.__name__
                filename, ext = os.path.basename(path).split('.')

                AudioProcessor.plot(
                    sample=sample,
                    n_fft=n_fft,
                    title=f"{yAxisMode} {name} window spectrogram [{ms}ms]",
                    outputFilePath=f"{self.__outputPath}/{filename}_{name}_{yAxisMode}_{ms}.png",
                    yAxisMode=yAxisMode
                )

    def noiseFilter(self, seconds: int, yAxisMode='log'):
        for path in self.samplesPaths:
            sample, sr = librosa.load(path)

            n_fft = int(seconds * sr)
            ms = int(seconds * 1000)

            sample = signal.wiener(sample)


            AudioProcessor.plot(
                sample=sample,
                title=f"filtered spectrogram [{ms}ms]",
                outputFilePath=f"{self.__outputPath}/filtered_{ms}.png",
                yAxisMode=yAxisMode
            )

            sf.write(
                f"{self.__outputPath}/filtered.wav",
                sample,
                sr,
                subtype='PCM_24'
            )
