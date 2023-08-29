import numpy
import os

from PIL import Image, ImageDraw
from images_processor import ImagesProcessor
from lab_5.src.image_info import ImageInfo


class Segmentator():
    def __init__(
        self,
        inputFolderPath: str,
        outputLettersFolderPath: str,
        outputProfilesFolderPath: str,
        minThreshold=0,
    ) -> None:
        self.__minThreshold = minThreshold
        self.__inputFolderPath = inputFolderPath
        self.__outputLettersFolderPath = outputLettersFolderPath
        self.__outputProfilesFolderPath = outputProfilesFolderPath

    def segment(self, axis: str):
        images = ImagesProcessor.getInputPathsFromFolder(
            self.__inputFolderPath)
        for path in images:
            info = ImageInfo(path)
            img = info.image

            if axis == 'vertical':
                info.saveProfileImages(self.__outputProfilesFolderPath)
            horizontal, vertical = info.getProfiles(reverseY=False)

            width, height = img.size

            if axis == 'vertical':
                segments = []
                prevCount = horizontal.count(0)

                if prevCount > self.__minThreshold:
                    segments.append(0)

                for i in range(1, width):
                    count = horizontal.count(i)

                    if prevCount <= self.__minThreshold and count > self.__minThreshold:
                        segments.append(i)

                    if prevCount > self.__minThreshold and count <= self.__minThreshold:
                        segments.append(i)

                    prevCount = count

                if len(segments) % 2 != 0:
                    segments.append(width - 1)

                for i in range(0, len(segments), 2):
                    name, ext = os.path.basename(path).split('.')
                    cropped = img.crop(
                        (segments[i], 0, segments[i + 1], height)
                    )
                    folder = f"{self.__outputLettersFolderPath}/{axis}"
                    filename = f"{name}_{str(i // 2 + 1).zfill(2)}.{ext}"
                    ImagesProcessor._createFolder(folder)
                    cropped.save(f"{folder}/{filename}")

            if axis == 'horizontal':
                segments = []
                prevCount = vertical.count(0)

                if prevCount > self.__minThreshold:
                    segments.append(0)

                for i in range(1, height):
                    count = vertical.count(i)
                    if prevCount <= self.__minThreshold and count > self.__minThreshold:
                        segments.append(i)

                    if prevCount > self.__minThreshold and count <= self.__minThreshold:
                        segments.append(i)

                    prevCount = count

                if len(segments) % 2 != 0:
                    segments.append(height - 1)

                print(segments)

                for i in range(0, len(segments), 2):
                    name, ext = os.path.basename(path).split('.')
                    cropped = img.crop(
                        (0, segments[i], width, segments[i + 1])
                    )
                    folder = f"{self.__outputLettersFolderPath}/{axis}"
                    filename = f"{name}.{ext}"
                    ImagesProcessor._createFolder(folder)
                    cropped.save(f"{folder}/{filename}")
