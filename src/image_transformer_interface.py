import numpy


class ImageTransformerInterface:
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        raise NotImplementedError()
