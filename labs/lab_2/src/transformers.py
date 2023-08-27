import numpy
from numpy.lib.function_base import average

from image_transformer_interface import ImageTransformerInterface
from overrides import override


class GrayscaleTransformer(ImageTransformerInterface):
    """Transforms image to grayscale"""

    def __init__(self, grayFromRGB) -> None:
        self.grayFromRGB = grayFromRGB

    @staticmethod
    def photoshopGrayColor(rgb: list[int]) -> int:
        R, G, B = rgb
        return 0.3 * R + 0.59 * G + 0.11 * B

    @staticmethod
    def avgGrayColor(rgb: list[int]) -> int:
        R, G, B = [int(color) for color in rgb]
        return (R + G + B) / 3

    @override
    def imageNameSuffix(self) -> str:
        if self.grayFromRGB == GrayscaleTransformer.photoshopGrayColor:
            return "Photoshop"
        if self.grayFromRGB == GrayscaleTransformer.avgGrayColor:
            return "Avg"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        transformed = numpy.ndarray(shape=(width, height))

        for i in range(width):
            for j in range(height):
                transformed[i][j] = self.grayFromRGB(pixels[i][j])

        return transformed, "L"


class GlobalBinzrizationTransformer(ImageTransformerInterface):
    """Binarizes a grayscale image via global threshold"""

    def __init__(self, threshold) -> None:
        self.threshold = threshold

    @override
    def imageNameSuffix(self) -> str:
        return f"Global_{str(self.threshold).zfill(3)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        transformed = numpy.ndarray(shape=(width, height))

        for i in range(width):
            for j in range(height):
                if pixels[i][j] > self.threshold:
                    transformed[i][j] = 255
                else:
                    transformed[i][j] = 0

        return transformed, "L"


class HistogramBinarizationTransformer(ImageTransformerInterface):
    """Binarizes a grayscale image"""

    def __init__(self, bins: int, threshold: int) -> None:
        self.bins = bins
        self.threshold = threshold

    @override
    def imageNameSuffix(self) -> str:
        return f"Histogram_{str(self.bins).zfill(3)}_{str(self.threshold)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        transformed = numpy.ndarray(shape=(width, height))

        histogram = [0] * 256
        binned = [0] * self.bins

        for i in range(width):
            for j in range(height):
                gray = pixels[i][j]
                histogram[gray] += 1

        for i in range(self.bins):
            colorsPerBin = int(256 / self.bins)
            start = i * colorsPerBin
            bin = histogram[start : (start + colorsPerBin)]
            maximum = max(bin)
            minimum = min(bin)
            # binned[i] = int((maximum - minimum) / 2)
            binned[i] = int(average(bin))

        leftOffset = 0
        rightOffset = 0

        for i in range(len(binned) // 2):
            start = i
            end = len(binned) - 1 - i

            left = binned[start]
            right = binned[end]

            if leftOffset == 0 and left > self.threshold:
                leftOffset = start

            if rightOffset == 0 and right > self.threshold:
                rightOffset = end

            if leftOffset != 0 and rightOffset != 0:
                break

        sliced = binned[leftOffset:rightOffset]
        while len(sliced) > 1:
            center = len(sliced) // 2

            start = center
            if len(sliced) % 2 != 0:
                start += 1

            left = sum(sliced[:center])
            right = sum(sliced[start:])

            print(left, "vs", right, sliced)

            if left > right:
                sliced = sliced[1:]
                leftOffset += 1
            elif left < right:
                sliced = sliced[:-1]
                rightOffset += 1
            else:
                break

        k = int((leftOffset + len(sliced) // 2) / self.bins * 256.0)
        print("k", k)

        for i in range(width):
            for j in range(height):
                gray = pixels[i][j]
                if gray > k:
                    transformed[i][j] = 255
                else:
                    transformed[i][j] = 0

        return transformed, "L"
