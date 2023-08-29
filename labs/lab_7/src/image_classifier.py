from functools import cache
import math
import csv 

from PIL import Image
from images_processor import ImagesProcessor
from lab_5.src.image_info import ImageInfo


class ImageClassifier:
    def __init__(self, dataCsvPath: str, inputImagesFolderPath: str) -> None:
        self.__inputImagesFolderPath = inputImagesFolderPath
        self.__dataCsvPath = dataCsvPath
        self.__baseLettersData = []
        self._loadLettersData()

    def _loadLettersData(self):
        with open(self.__dataCsvPath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                line = line.split(',')
                self.__baseLettersData.append(line)

        self.__baseLettersData = [
            data
            for data in self.__baseLettersData if len(data) > 1
        ]

    def printResults(self, limit=None):
        paths, lettersDistances = self.classificate()

        for i in range(len(paths)):
            print(f"\nImage {paths[i]}")
            letterDistances = lettersDistances[i]

            if limit != None:
                letterDistances = letterDistances[:limit]


            for letterDistance in letterDistances:
                print(letterDistance)
    
    def exportResultsToCsv(self, outputCsvFilePath: str):
        paths, lettersDistances = self.classificate()

        lettersDistances = [
            [
                (letterDistance[0], str(letterDistance[1])) 
                for letterDistance in letterDistances
            ] 
            for letterDistances in lettersDistances 
        ]

        with open(outputCsvFilePath, "w+", encoding="utf-8") as file:
            writer = csv.writer(file, dialect='excel', delimiter=";")
            writer.writerows(lettersDistances)

    @cache
    def classificate(self):
        normalizedColumns = [4, 5, 6, 7, 11, 12, 15, 16]
        paths = ImagesProcessor.getInputPathsFromFolder(self.__inputImagesFolderPath)

        lettersDistances = []

        maxDistance = None        

        for path in paths:
            info = ImageInfo(path)
            letterData = info.getInfo()

            letterDistances = []
            maxDistance = None

            for baseLetterData in self.__baseLettersData[1:]:
                letter = baseLetterData[0]

                diffs = [
                    (letterData[i] - float(baseLetterData[1:][i])) ** 2
                    for i in range(len(letterData)) if i in normalizedColumns
                ]

                distance = math.sqrt(sum(diffs))

                if maxDistance == None or distance > maxDistance:
                    maxDistance = distance

                letterDistances.append((letter, round(1 - distance / maxDistance, 3)))

            lettersDistances.append(letterDistances)
                
        sortedNormalizedLettersDistances = [
            sorted(letterDistances, key=lambda distances: distances[1], reverse=True)
            for letterDistances in lettersDistances 
        ]

        return paths, sortedNormalizedLettersDistances