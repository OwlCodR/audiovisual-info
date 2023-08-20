import os
import time
import numpy
import shutil

from pathlib import Path
from image_transformer_interface import ImageTransformerInterface
from PIL import Image


class ImagesProcessor:
    """Applies transformer's method to the input images"""

    @staticmethod
    def fromImagesList(
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via list of images"""
        return ImagesProcessor(
            ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
            outputFolderPath,
            supportImageTypes,
        )

    @staticmethod
    def fromImagesFolder(
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via images folder"""
        return ImagesProcessor(
            ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
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

    def transformByAll(self, transformers: list[ImageTransformerInterface]):
        for transformer in transformers:
            self.transform(transformer)

    def transform(self, transformer: ImageTransformerInterface):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        transformerName = type(transformer).__name__
        dir = f"{self.__outputFolderPath}/{transformerName}"

        if (os.path.exists(dir)):
            shutil.rmtree(dir)
        Path(dir).mkdir()

        for imagePath in self.__inputPaths:
            img = Image.open(imagePath)

            print(
                f"\nTransforming image {img.mode}, '{imagePath}' by [{transformerName}]"
            )

            pixels = numpy.array(img)

            print(f"Input image shape: {pixels.shape}")
            print(f"Processing {pixels.size} pixels...")
            tarnsformTime = time.time()
            pixels = transformer.transform(pixels)
            print(f"Finished in {int(time.time() - tarnsformTime)}s")
            print(f"Output image shape: {pixels.shape}")

            img = Image.fromarray(pixels.astype(numpy.uint8), img.mode)

            imgPath = f"{dir}/{os.path.basename(imagePath)}"
            img.save(imgPath)

    def combine(self, transformers: list[ImageTransformerInterface]):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        path = f"{self.__outputFolderPath}/Combined/"

        shutil.rmtree(path)
        Path(path).mkdir(exist_ok=True)

        for imagePath in self.__inputPaths:
            inputImg = Image.open(imagePath)
            inputImgName = os.path.basename(imagePath)
            images = [inputImg]

            for transformer in transformers:
                transformerName = type(transformer).__name__
                dir = f"{self.__outputFolderPath}/{transformerName}"
                imgPath = f"{dir}/{inputImgName}"
                images.append(Image.open(imgPath))

            print(f"\nCombine images...")
            for image in images:
                print(image.filename)

            totalWidth = max([image.size[0] for image in images])
            maxHeight = sum([image.size[1] for image in images])

            combined = Image.new(inputImg.mode, (totalWidth, maxHeight))

            padding = 10
            offset = 0
            for img in images:
                combined.paste(img, (0, offset))
                offset += img.size[1] + padding

            combined.save(f"{path}/{inputImgName}")
            print("Combined!")
