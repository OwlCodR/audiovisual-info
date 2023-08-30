import numpy
import math
import colorsys

from image_transformer_interface import ImageTransformerInterface
from overrides import override


class HaralicMatrixTransformer(ImageTransformerInterface):
    """ Transforms grayscale image to haralic matrix """

    COLORS_COUNT = 256

    def __init__(self, d: int, phi: list[int]) -> None:
        self.__d = d
        self.__phi = phi

    def getSumP(self, i=None, j=None):
        sum = 0

        for a in range(self.COLORS_COUNT):
            if i != None and j != None:
                sum += self.__transformed[i][j]
            elif i != None:
                sum += self.__transformed[i][a]
            elif j != None:
                sum += self.__transformed[a][j]

        return sum

    def printCORR(self):
        mu = 0
        dispersion = 0

        for i in range(self.COLORS_COUNT):
            mu += i * self.getSumP(i=i)

        for i in range(self.COLORS_COUNT):
            dispersion += (i - mu) ** 2 * self.getSumP(i=i)

        result = 0

        for i in range(self.COLORS_COUNT):
            for j in range(self.COLORS_COUNT):
                result += (i - mu) * (j - mu) * self.getSumP(i, j)

        corr = 1 / dispersion * result

        print(f'CORR = {corr}')

    @override
    def imageNameSuffix(self) -> str:
        return "Haralic"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        height = pixels.shape[0]
        width = pixels.shape[1]

        transformed = numpy.full(
            shape=(self.COLORS_COUNT, self.COLORS_COUNT),
            fill_value=0,
            dtype=int,
        )

        for y in range(height):
            for x in range(width):
                base = pixels[y][x]

                for phi in self.__phi:
                    dx = numpy.cos(numpy.deg2rad(phi))
                    dy = numpy.sin(numpy.deg2rad(phi))

                    dx = int(dx) + (dx > 0) - (dx < 0)
                    dy = int(dy) + (dy > 0) - (dy < 0)

                    i = y + dy * self.__d
                    j = x + dx * self.__d

                    if i > 0 and i < height and j > 0 and j < width:
                        current = pixels[i][j]
                        transformed[base][current] += 1
        self.__transformed = transformed
        # self.printCORR()
        return transformed, "L"

class LinearLightnessTransformer(ImageTransformerInterface):
    """ Transforms RGB image to image with bigger lightness """

    def __init__(self, gmin: int, gmax: int) -> None:
        self.__gmin = gmin / 255
        self.__gmax = gmax / 255

    @override
    def imageNameSuffix(self) -> str:
        return "Lightness"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        height = pixels.shape[0]
        width = pixels.shape[1]
        colors = pixels.shape[2]

        transformed = numpy.ndarray(shape=(height, width, colors))
        
        fmax = None
        fmin = None

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y][x]
                h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
                if fmax == None or l > fmax:
                    fmax = l
                elif fmin == None or l < fmin:
                    fmin = l

        delta = fmax - fmin
        a = (self.__gmax - self.__gmin) / delta
        b = (self.__gmin * fmax - self.__gmax * fmin) / delta

        for y in range(height):
            for x in range(width):
                red, green, blue = pixels[y][x]
                hls = colorsys.rgb_to_hls(red / 255.0, green / 255.0, blue / 255.0)
                l = a * hls[1] + b
                red, green, blue = colorsys.hls_to_rgb(hls[0], l, hls[2])
                transformed[y][x] = (red * 255, green * 255, blue * 255)
        return transformed, "RGB"
