import os
import time
import numpy
import shutil

from pathlib import Path
from image_transformer_interface import ImageTransformerInterface
from PIL import Image, ImageFont, ImageDraw


class ImagesProcessor:
    """Applies transformer's method to the input images"""

    @staticmethod
    def fromImagesList(
        inputFolderPath: str,
        outputFolderPath: str,
        combinedFolderPath: str,
        markdownFilePath: str,
        markdownImagesFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via list of images"""
        return ImagesProcessor(
            inputPaths=ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
            outputFolderPath=outputFolderPath,
            combinedFolderPath=combinedFolderPath,
            markdownFilePath=markdownFilePath,
            markdownImagesFolderPath=markdownImagesFolderPath,
            supportImageTypes=supportImageTypes,
        )

    @staticmethod
    def fromImagesFolder(
        inputFolderPath: str,
        outputFolderPath: str,
        combinedFolderPath: str,
        markdownFilePath: str,
        markdownImagesFolderPath: str,
        supportImageTypes: list[str],
    ):
        """Initialization via images folder"""
        return ImagesProcessor(
            inputPaths=ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
            outputFolderPath=outputFolderPath,
            combinedFolderPath=combinedFolderPath,
            markdownFilePath=markdownFilePath,
            markdownImagesFolderPath=markdownImagesFolderPath,
            supportImageTypes=supportImageTypes,
        )

    def __init__(
        self,
        inputPaths: list[str],
        outputFolderPath: str,
        combinedFolderPath: str,
        markdownFilePath: str,
        markdownImagesFolderPath: str,
        supportImageTypes=["png", "bmp"],
    ):
        """Default constructor"""
        self.__inputPaths = inputPaths
        self.__outputFolderPath = outputFolderPath
        self.__combinedFolderPath = combinedFolderPath
        self.__markdownFilePath = markdownFilePath
        self.__markdownImagesFolderPath = markdownImagesFolderPath
        self.__supportImageTypes = supportImageTypes

    @staticmethod
    def _getInputPathsFromFolder(
        folderPath: str,
        supportImageTypes: list[str],
        includeFolderPath=True,
    ) -> list[str]:
        inputPaths = []
        for supportedType in supportImageTypes:
            for file in os.listdir(folderPath):
                if file.endswith(f".{supportedType}"):
                    if includeFolderPath:
                        inputPaths.append(f"{folderPath}/{file}")
                    else:
                        inputPaths.append(file)
        return inputPaths

    @staticmethod
    def _createFolder(dir: str):
        if os.path.exists(dir):
            shutil.rmtree(dir)
        Path(dir).mkdir()

    def transformByAll(self, transformers: list[ImageTransformerInterface]):
        for transformer in transformers:
            self.transform(transformer)

    def transform(self, transformer: ImageTransformerInterface):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        folderName = type(transformer).__name__ + transformer.folderSuffix()
        dir = f"{self.__outputFolderPath}/{folderName}"

        self._createFolder(dir)

        for imagePath in self.__inputPaths:
            img = Image.open(imagePath)
            pixels = numpy.array(img)

            print(f"\nTransforming image {img.mode}, '{imagePath}' by {folderName}")
            print(f"Input image shape: {pixels.shape}")
            print(f"Processing {pixels.size} pixels...")

            tarnsformTime = time.time()
            pixels, mode = transformer.transform(pixels)

            print(f"Output image shape: {pixels.shape}")
            print(f"Finished in {int(time.time() - tarnsformTime)}s")

            print(pixels.shape)
            img = Image.fromarray(pixels.astype(numpy.uint8), mode)

            imgPath = f"{dir}/{os.path.basename(imagePath)}"
            img.save(imgPath)

    def combine(self):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        self._createFolder(dir=self.__combinedFolderPath)

        for imagePath in self.__inputPaths:
            inputImgName = os.path.basename(imagePath)
            images = []
            paths = []

            folders = [
                f"{f.path}/{inputImgName}" for f in os.scandir(self.__outputFolderPath) if f.is_dir()
            ]

            for folder in folders:
                folder = folder.replace("\\", "/")
                if self.__combinedFolderPath not in folder:
                    images.append(Image.open(folder))
                    paths.append(folder)

            print(f"\nCombine images...")
            for image in images:
                print(image.filename)

            totalWidth = max([image.size[0] for image in images])
            maxHeight = sum([image.size[1] for image in images])

            padding = 10
            combined = Image.new("RGB", (totalWidth, maxHeight + padding * len(images)))

            offset = 0
            for i in range(len(images)):
                combined.paste(images[i], (0, offset))
                draw = ImageDraw.Draw(combined)
                font = ImageFont.truetype("fonts/sans-serif.ttf", 24)
                draw.text((10, offset), paths[i], (255, 0, 0), font=font)
                offset += images[i].size[1] + padding

            combined.save(f"{self.__combinedFolderPath}/{inputImgName}")
            print("Combined!")

    def addCombinedtoReadme(self):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        DIVIDER = "\n\n### **Examples**\n"

        content = str()

        print("Adding combined images to README.md...")
        with open(self.__markdownFilePath, "r") as file:
            content = file.read().split(DIVIDER)[0]

        with open(self.__markdownFilePath, "w") as file:
            images = ImagesProcessor._getInputPathsFromFolder(
                self.__combinedFolderPath, self.__supportImageTypes, False
            )
            lines = [content, DIVIDER]
            lines.extend(
                [
                    f"\n![]({self.__markdownImagesFolderPath}/{image})"
                    for image in images
                ]
            )
            file.writelines(lines)
        print("Added!")
