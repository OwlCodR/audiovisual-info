import numpy
from image_transformer_interface import ImageTransformerInterface
from overrides import override


class Transformer(ImageTransformerInterface):
    """ """

    def __init__(self, threshold) -> None:
        pass

    @override
    def imageNameSuffix(self) -> str:
        return ""

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
