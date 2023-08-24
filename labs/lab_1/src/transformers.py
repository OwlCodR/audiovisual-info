import numpy

from image_transformer_interface import ImageTransformerInterface
from overrides import override


class UpsamplingTransformer(ImageTransformerInterface):
    """Image interpolation"""

    def __init__(self, M: int) -> None:
        self.M = M

    @override
    def imageNameSuffix(self) -> str:
        return f"Interpolation_{str(self.M)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        M = self.M
        width = pixels.shape[0] * M
        height = pixels.shape[1] * M
        colors = 3

        transformed = numpy.ndarray(shape=(width, height, colors))

        width = transformed.shape[0]
        height = transformed.shape[1]

        for i in range(width):
            for j in range(height):
                transformed[i][j] = pixels[i // M][j // M][:colors]

        return transformed, 'RGB'


class DownsamplingTransformer(ImageTransformerInterface):
    """Image decimation"""

    def __init__(self, N: int) -> None:
        self.N = N

    @override
    def imageNameSuffix(self) -> str:
        return f"Decimation_{str(self.N)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        N = self.N
        width = pixels.shape[0] // N
        height = pixels.shape[1] // N
        colors = pixels.shape[2]

        transformed = numpy.ndarray(shape=(width, height, colors))

        width = transformed.shape[0]
        height = transformed.shape[1]

        for i in range(width):
            for j in range(height):
                transformed[i][j] = pixels[i * N][j * N]

        return transformed, 'RGB'


class ResamplingTransformer2Pass(ImageTransformerInterface):
    """Image resampling by 2 pass: interpolation and decimation"""

    def __init__(self, M: int, N: int) -> None:
        self.M = M
        self.N = N

    @override
    def imageNameSuffix(self) -> str:
        return f"ResamplingTwoPass_{str(self.M)}_{str(self.N)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        M = self.M
        N = self.N
        
        # Interpolation
                
        width = pixels.shape[0] * M
        height = pixels.shape[1] * M
        colors = pixels.shape[2]

        interpolated = numpy.ndarray(shape=(width, height, colors))

        width = interpolated.shape[0]
        height = interpolated.shape[1]

        for i in range(width):
            for j in range(height):
                interpolated[i][j] = pixels[i // M][j // M]
        
        # Decimation
        
        width = interpolated.shape[0] // N
        height = interpolated.shape[1] // N
        colors = interpolated.shape[2]

        decimated = numpy.ndarray(shape=(width, height, colors))

        for i in range(width):
            for j in range(height):
                decimated[i][j] = interpolated[i * N][j * N]

        return decimated, 'RGB'


class ResamplingTransformer1Pass(ImageTransformerInterface):
    """Image resampling by 1 pass"""

    def __init__(self, M: int, N: int) -> None:
        self.M = M
        self.N = N

    @override
    def imageNameSuffix(self) -> str:
        return f"ResamplingOnePass_{str(self.M)}_{str(self.N)}"

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        M = self.M
        N = self.N
        
        width = pixels.shape[0] * M // N
        height = pixels.shape[1] * M // N
        colors = pixels.shape[2]

        transformed = numpy.ndarray(shape=(width, height, colors))

        width = transformed.shape[0]
        height = transformed.shape[1]

        for i in range(width):
            for j in range(height):
                transformed[i][j] = pixels[i * N // M][j * N // M]

        return transformed, 'RGB'
