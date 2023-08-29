import numpy
from PIL import Image
from functools import cache
import matplotlib.pyplot as plot
import os
import csv


class ImageInfo:
    """Gets info about image"""

    def __init__(
        self,
        inputPath: str,
    ) -> None:
        img = Image.open(inputPath)
        print(f"\nGetting info of '{inputPath}', {img.size}")
        self.image = img
        self.__pixels = numpy.array(img)
        self.__inputPath = inputPath

    def __getQuarterMomentum(
        self, p: int, q: int, qx: int, qy: int, x_center=0, y_center=0
    ):
        height, width = self.__pixels.shape

        startX = width * qx // 2
        endX = width * (qx + 1) // 2
        startY = height * qy // 2
        endY = height * (qy + 1) // 2

        m = 0
        for y in range(startY, endY):
            for x in range(startX, endX):
                pixel = not self.__pixels[y][x]
                m += (x - x_center) ** p * (y - y_center) ** q * pixel
        return m

    @cache
    def __getMomentum(self, p: int, q: int, x_center=0, y_center=0):
        height, width = self.__pixels.shape

        m = 0
        for y in range(height):
            for x in range(width):
                pixel = not self.__pixels[y][x]
                m += (x - x_center) ** p * (y - y_center) ** q * pixel
        return m

    def __getWeight(self):
        """Returns the weight of image"""
        return self.__getMomentum(0, 0)

    def __getNormWeight(self):
        """Returns the specific weight of image"""
        height, width = self.__pixels.shape
        pixels = width * height
        return round(self.__getWeight() / pixels, 2)

    def __getNormWeights(self):
        """Returns the specific weight of every quarter of image"""
        weights = self.__getWeights()
        height, width = self.__pixels.shape
        pixels = width * height
        return [round(weight / (pixels // 4), 2) for weight in weights]

    def __getWeights(self):
        """Returns the weight of every quarter of image"""
        weights = []
        for qy in range(2):
            for qx in range(2):
                weights.append(self.__getQuarterMomentum(p=0, q=0, qx=qx, qy=qy))

        return weights

    def __getWeightCenter(self):
        """Returns the center of weight of image"""
        height, width = self.__pixels.shape

        cx = self.__getMomentum(p=1, q=0)
        cy = self.__getMomentum(p=0, q=1)

        weight = self.__getWeight()

        x = round(cx / weight, 2)
        y = round(cy / weight, 2)

        if x == 0:
            x = round(width / 2, 2)
        if y == 0:
            y = round(height / 2, 2)

        return x, y

    def __getNormWeightCenter(self):
        """Returns normalized center of weight of image"""
        height, width = self.__pixels.shape

        x, y = self.__getWeightCenter()

        x = round((x - 1) / (width - 1), 2)
        y = round((y - 1) / (height - 1), 2)

        return x, y

    def __getAxisMomentum(self):
        x, y = self.__getWeightCenter()

        xAxis = self.__getMomentum(p=2, q=0, x_center=x)
        yAxis = self.__getMomentum(p=0, q=2, y_center=y)

        return round(xAxis, 2), round(yAxis, 2)

    def __getNormAxisMomentum(self):
        x, y = self.__getAxisMomentum()
        n = self.__getWeight() ** 2

        return round(x / n, 2), round(y / n, 2)

    def getProfiles(self, reverseY=True):
        height, width = self.__pixels.shape

        horizontal = []
        vertical = []

        for y in range(height):
            for x in range(width):
                if self.__pixels[y][x] == 0:
                    dy = height - y
                    if not reverseY:
                        dy = y
                    horizontal.append(x)
                    vertical.append(dy)
        
        return horizontal, vertical

    def saveProfileImages(self, path: str):
        horizontal, vertical = self.getProfiles()

        name, extension = os.path.basename(self.__inputPath).split(".")

        plot.hist(horizontal, bins=len(set(horizontal)))
        plot.ylabel("Count")
        plot.xlabel("Line Number")
        plot.savefig(f"{path}/{name}_vertical.{extension}")

        plot.clf()

        plot.hist(vertical, bins=len(set(vertical)), orientation="horizontal")
        plot.ylabel("Line Number")
        plot.xlabel("Count")
        plot.savefig(f"{path}/{name}_horizontal.{extension}")

        plot.close()

    def createCsv(self, outputCsvPath: str):
        with open(outputCsvPath, "w+") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(
                [
                    "Letter",
                    "WeightQuarter1",
                    "WeightQuarter2",
                    "WeightQuarter3",
                    "WeightQuarter4",
                    "NormWeightQuarter1",
                    "NormWeightQuarter2",
                    "NormWeightQuarter3",
                    "NormWeightQuarter4",
                    "TotalNormWeight",
                    "XWeightCenter",
                    "YWeightCenter",
                    "XNormWeightCenter",
                    "YNormWeightCenter",
                    "XAxisMomentum",
                    "YAxisMomentum",
                    "XNormAxisMomentum",
                    "YNormAxisMomentum",
                ]
            )

    def exportCsv(self, letter: str, path: str):
        with open(path, "a+", encoding="utf8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([letter] + self.getInfo())

    def getInfo(self):
        w1, w2, w3, w4 = self.__getWeights()
        nw1, nw2, nw3, nw4 = self.__getNormWeights()
        totalNormWeight = self.__getNormWeight()
        xc, yc = self.__getWeightCenter()
        nxc, nyc = self.__getNormWeightCenter()
        xa, ya = self.__getAxisMomentum()
        nxa, nya = self.__getNormAxisMomentum()
        
        return [ w1, w2, w3, w4, nw1, nw2, nw3, nw4, totalNormWeight, xc, yc, nxc, nyc, xa, ya, nxa, nya ]

    def printInfo(self):
        print("Вес каждой четверти:", self.__getWeights())
        print("Удельный вес каждой четверти:", self.__getNormWeights())
        print("Удельный вес всего изображения:", self.__getNormWeight())
        print("Центр тяжести:", self.__getWeightCenter())
        print("Нормированный центр тяжести:", self.__getNormWeightCenter())
        print("Осевые моменты инерции:", self.__getAxisMomentum())
        print("Нормированные осевые моменты инерции:", self.__getNormAxisMomentum())
