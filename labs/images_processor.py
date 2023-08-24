import os
import time
import numpy

from pathlib import Path
from image_transformer_interface import ImageTransformerInterface
from PIL import Image, ImageFont, ImageDraw, ImageChops


class ImagesProcessor:
    """Applies transformer's method to the input images"""

    @staticmethod
    def fromImagesList(
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes=["png", "bmp"],
    ):
        """Initialization via list of images"""
        return ImagesProcessor(
            inputPaths=ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
            outputFolderPath=outputFolderPath,
        )

    @staticmethod
    def fromImagesFolder(
        inputFolderPath: str,
        outputFolderPath: str,
        supportImageTypes=["png", "bmp"],
    ):
        """Initialization via images folder"""
        return ImagesProcessor(
            inputPaths=ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes
            ),
            outputFolderPath=outputFolderPath,
        )

    def __init__(
        self,
        inputPaths: list[str],
        outputFolderPath: str,
    ):
        """Default constructor"""
        self.__inputPaths = inputPaths
        self.__outputFolderPath = outputFolderPath

    @staticmethod
    def _getInputPathsFromFolder(
        folderPath: str,
        supportImageTypes=["png", "bmp"],
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
        if not os.path.exists(dir):
            Path(dir).mkdir()

    def transformByAll(self, transformers: list[ImageTransformerInterface]):
        for transformer in transformers:
            self.transform(transformer)

    def transform(self, transformer: ImageTransformerInterface):
        if len(self.__inputPaths) == 0:
            raise Exception("No files to transform")

        self._createFolder(self.__outputFolderPath)

        for inputImagePath in self.__inputPaths:
            img = Image.open(inputImagePath)
            pixels = numpy.array(img)

            print(f"\nTransforming image {img.mode}, '{inputImagePath}'")
            print(f"Input image shape: {pixels.shape}")
            print(f"Processing {pixels.size} pixels...")

            tarnsformTime = time.time()
            pixels, mode = transformer.transform(pixels)

            print(f"Output image shape: {pixels.shape}")
            print(f"Finished in {int(time.time() - tarnsformTime)}s")

            img = Image.fromarray(pixels.astype(numpy.uint8), mode)

            imgBaseName, extension = os.path.basename(inputImagePath).split(".")
            imgName = f"{imgBaseName}_{transformer.imageNameSuffix()}.{extension}"
            imgPath = f"{self.__outputFolderPath}/{imgName}"
            img.save(imgPath)

            print(pixels.shape, imgPath)

    @staticmethod
    def __saveCombinedImage(images: list, names: list, path: str):
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
            font = ImageFont.truetype("fonts/sans-serif.ttf", 28)
            draw.text((10, offset), names[i], (255, 0, 0), font=font)
            offset += images[i].size[1] + padding

        combined.save(path)
        print("Combined!")

    @staticmethod
    def __saveXorImage(images: list, names: list, path: str):
        print(images)
        if len(images) < 2:
            print("Warning! No image to xor!")

        print(f"\nXor images...")
        for image in images:
            print(image.filename)

        base = images[0]

        for i in range(1, len(images)):
            xor = ImageChops.logical_xor(
                base.convert("1", dither=Image.NONE),
                images[i].convert("1", dither=Image.NONE),
            )
            xor.save(f"{path}/{names[i]}")

        print("Done!")

    @staticmethod
    def combine(
        baseImagesFolderPath: str,
        transformedFoldersPaths: list[str],
        outputFolderPath: str,
    ):
        ImagesProcessor._createFolder(dir=outputFolderPath)

        baseImagesPaths = ImagesProcessor._getInputPathsFromFolder(
            baseImagesFolderPath,
        )
        transformedImagesPaths = []

        for transformedFolder in transformedFoldersPaths:
            images = ImagesProcessor._getInputPathsFromFolder(transformedFolder)
            transformedImagesPaths.extend(images)

        for baseImagePath in baseImagesPaths:
            baseName = os.path.basename(baseImagePath)
            images = [Image.open(baseImagePath)]
            names = [baseName]

            for transformedImagePath in transformedImagesPaths:
                transformedName = os.path.basename(transformedImagePath)
                if baseName.split(".")[0] in transformedName:
                    images.append(Image.open(transformedImagePath))
                    names.append(transformedName)

            ImagesProcessor.__saveCombinedImage(
                images, names, f"{outputFolderPath}/{baseName}"
            )

    @staticmethod
    def addImagesToReadme(
        inputFolderPath: str,
        outputPath: str,
        relativePathFromOutputToInput: str,
        supportImageTypes=["png", "bmp"],
        outputFilename="README.md",
        divider="\n\n### **Examples**\n",
    ):
        print("Adding combined images to README.md...")

        content = str()
        outputFilePath = f"{outputPath}/{outputFilename}"

        with open(outputFilePath, "r") as file:
            content = file.read().split(divider)[0]

        with open(outputFilePath, "w") as file:
            images = ImagesProcessor._getInputPathsFromFolder(
                inputFolderPath, supportImageTypes, False
            )

            lines = [content, divider]
            lines.extend(
                [f"\n![]({relativePathFromOutputToInput}/{image})" for image in images]
            )
            file.writelines(lines)
        print("Added!")

    @staticmethod
    def xorImages(
        baseImagesFolderPath: str,
        toXorFolderPath: str,
        outputFolderPath: str,
    ):
        ImagesProcessor._createFolder(dir=outputFolderPath)

        baseImagesPaths = ImagesProcessor._getInputPathsFromFolder(
            baseImagesFolderPath,
        )
        transformedImagesPaths = []

        images = ImagesProcessor._getInputPathsFromFolder(toXorFolderPath)
        transformedImagesPaths.extend(images)

        for baseImagePath in baseImagesPaths:
            name, extension = os.path.basename(baseImagePath).split(".")

            images = [Image.open(baseImagePath)]
            names = [baseImagePath]

            for transformedImagePath in transformedImagesPaths:
                transformedName = os.path.basename(transformedImagePath)
                if name in transformedName:
                    prefix, suffix = os.path.basename(transformedImagePath).split(".")
                    images.append(Image.open(transformedImagePath))
                    names.append(f"{prefix}_xor.{suffix}")

            ImagesProcessor.__saveXorImage(images, names, outputFolderPath)
