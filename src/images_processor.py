import os

import numpy
from image_transformer_interface import ImageTransformerInterface
from PIL import Image


class ImagesProcessor:
    """Applies transformer's method to the input images"""

    @classmethod
    def fromImagesList(
        selfClass,
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via list of images"""
        return selfClass(
            selfClass,
            selfClass._getInputPathsFromFolder(inputFolderPath, supportImageTypes),
            outputFolderPath,
            supportImageTypes,
        )

    @classmethod
    def fromImagesFolder(
        selfClass,
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via list of images"""
        return selfClass(
            selfClass._getInputPathsFromFolder(inputFolderPath, supportImageTypes),
            outputFolderPath,
            supportImageTypes,
        )

    def __init__(
        self,
        inputPaths: list[str],
        outputFolderPath: str,
        supportImageTypes=["png", "bmp"],
    ):
        """Default constructor"""
        self.__inputPaths = inputPaths
        self.__outputFolderPath = outputFolderPath
        self.supportImageTypes = supportImageTypes

    @staticmethod
    def _getInputPathsFromFolder(
        folderPath: str, supportImageTypes: list[str]
    ) -> list[str]:
        inputPaths = []
        for supportedType in supportImageTypes:
            for file in os.listdir(folderPath):
                if file.endswith(f".{supportedType}"):
                    inputPaths.append(f"{folderPath}/{file}")
        return inputPaths

    def transformImages(self, transformer: ImageTransformerInterface):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        for imagePath in self.__inputPaths:
            img = Image.open(imagePath)
            print(f"Transforming image {img.size}, {img.mode} {imagePath}")

            pixels = numpy.array(img)
            pixels = transformer.transform(pixels)

            img = Image.fromarray(pixels.astype(numpy.uint8), img.mode)
            img.save(f"{self.__outputFolderPath}/{os.path.basename(imagePath)}")
