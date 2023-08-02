from abc import ABC, abstractmethod
import numpy


class ImageTransformerInterface(ABC):
    @abstractmethod
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        pass
