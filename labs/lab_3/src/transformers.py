import numpy
from overrides import override
from image_transformer_interface import ImageTransformerInterface


class MorphologicalOpeningTransformer(ImageTransformerInterface):
    """Erosion-Dilation transformation (Сжатие-Расширение)"""

    def __init__(self, aperture: numpy.ndarray, isWhite: bool) -> None:
        self.aperture = aperture
        self.isWhite = isWhite

    @override
    def imageNameSuffix(self) -> str:
        if self.isWhite:
            return "white"
        return "black"

    @override
    def transform(self, pixels: numpy.ndarray):
        pixels = self.__erosion(pixels)
        pixels = self.__dilation(pixels)
        return pixels, "L"

    def __morphological(
        self,
        pixels: numpy.ndarray,
        target: int,
    ) -> numpy.ndarray:
        width = pixels.shape[0]
        height = pixels.shape[1]

        transformed = pixels.copy()

        apertureWidth = len(self.aperture)
        apertureHeight = len(self.aperture[0])
        centerWidth, centerHeight = apertureWidth // 2, apertureHeight // 2

        for i in range(centerWidth, width - centerWidth):
            for j in range(centerHeight, height - centerHeight):
                colors = []

                for row in range(apertureWidth):
                    for column in range(apertureHeight):
                        diffX = row - centerWidth
                        diffY = column - centerHeight

                        if self.aperture[row][column] == 1:
                            colors.append(pixels[i + diffX][j + diffY])
                if target in colors:
                    transformed[i][j] = target
        return transformed

    def __erosion(self, pixels: numpy.ndarray) -> numpy.ndarray:
        k = int(not self.isWhite) * 255
        return self.__morphological(pixels, k)

    def __dilation(self, pixels: numpy.ndarray) -> numpy.ndarray:
        k = int(self.isWhite) * 255
        return self.__morphological(pixels, k)
