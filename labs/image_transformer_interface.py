import numpy


class ImageTransformerInterface:
    def folderSuffix(self) -> str:
        return ''
    
    def transform(self, pixels: numpy.ndarray):
        raise NotImplementedError()
