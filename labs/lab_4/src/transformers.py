import numpy
import math
from overrides.overrides import override
from image_transformer_interface import ImageTransformerInterface


class OutlineRobertsTransformer(ImageTransformerInterface):
    """Shows the image outlines via roberts operator"""

    def __init__(self, matrix: str) -> None:
        self.matrix = matrix

    @override
    def imageNameSuffix(self) -> str:
        return self.matrix

    @override
    def transform(self, pixels: numpy.ndarray) -> numpy.ndarray:
        transformed = pixels.copy()
        
        width = transformed.shape[0]
        height = transformed.shape[1]

        windowWidth = 3
        windowHeight = 3

        centerWidth = windowWidth // 2
        centerHeight = windowHeight // 2

        for i in range(centerWidth, width - centerWidth):
            for j in range(centerHeight, height - centerHeight):
                z5 = int(transformed[i][j])
                z6 = int(transformed[i][j + 1])
                z8 = int(transformed[i + 1][j])
                z9 = int(transformed[i + 1][j + 1])
                
                Gx = z9 - z5
                Gy = z8 - z6
                
                if self.matrix == 'Gx':
                    transformed[i][j] = Gx
                elif self.matrix == 'Gy':
                    transformed[i][j] = Gy
                elif self.matrix == 'G':
                    G = math.sqrt(Gx ** 2 + Gy ** 2)
                    transformed[i][j] = G

        maxBrightness = numpy.amax(transformed)

        # Нормализация
        for i in range(width):
            for j in range(height):
                transformed[i][j] = transformed[i][j] / maxBrightness * 255

        return transformed, "L"