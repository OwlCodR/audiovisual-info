import numpy


class ImageTransformerInterface:
    def imageNameSuffix(self) -> str:
        return "transformed"

    def transform(self, pixels: numpy.ndarray):
        raise NotImplementedError()
