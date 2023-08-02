import numpy

from image_transformer_interface import ImageTransformerInterface


class InterpolationTransformer(ImageTransformerInterface):
    def __init__(self, N: int) -> None:
        self.N = N
    
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        return pixels

class DecimationTransformer(ImageTransformerInterface):
    def __init__(self, N: int) -> None:
        self.N = N
        
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        return pixels
    
class ResamplingTransformer1Pass(ImageTransformerInterface):
    def __init__(self, M: int, N: int) -> None:
        self.K = M / N
        
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        return pixels

class ResamplingTransformer2Pass(ImageTransformerInterface):
    def __init__(self, M: int, N: int) -> None:
        self.K = M / N

    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        return pixels