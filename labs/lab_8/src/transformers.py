import numpy
import math

from image_transformer_interface import ImageTransformerInterface
from overrides import override


class HaralicMatrixTransformer(ImageTransformerInterface):
    """ Transforms image to haralic matrix """

    def __init__(self, d: int, phi: list[int]) -> None:
        self.__d = d
        self.__phi = phi

    @override
    def imageNameSuffix(self) -> str:
        return "haralic"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        COLORS_COUNT = 256

        height = pixels.shape[0]
        width = pixels.shape[1]

        transformed = numpy.full(shape=(COLORS_COUNT, COLORS_COUNT), fill_value=0, dtype=int)

        for y in range(height):
            for x in range(width):
                base = pixels[y][x]

                for phi in self.__phi:
                    dx = numpy.cos(numpy.deg2rad(phi))
                    dy = numpy.sin(numpy.deg2rad(phi))

                    dx = int(dx) + (dx > 0) - (dx < 0)
                    dy = int(dy) + (dy > 0) - (dy < 0)
                    
                    i = y + dy
                    j = x + dx

                    if i > 0 and i < height and j > 0 and j < width:
                        current = pixels[i][j]
                        transformed[base][current] +=  1
        return transformed, "L"