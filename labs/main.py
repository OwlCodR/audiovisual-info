from images_processor import ImagesProcessor
from lab_1.src.transformers import *
from lab_2.src.transformers import (
    GlobalBinzrizationTransformer,
    GrayscaleTransformer,
    HistogramBinarizationTransformer,
)
from lab_3.src.transformers import MorphologicalOpeningTransformer
from lab_4.src.transformers import OutlineRobertsTransformer
from lab_5.src.image_info import ImageInfo
from lab_5.src.letters_generator import LettersImageGenerator


def lab1():
    processor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_1/input",
        outputFolderPath="./labs/lab_1/output",
        supportImageTypes=["png"],
    )

    transformers = [
        UpsamplingTransformer(M=2),
        DownsamplingTransformer(N=4),
        ResamplingTransformer1Pass(M=2, N=4),
        ResamplingTransformer2Pass(M=2, N=4),
    ]

    processor.transformByAll(transformers)

    ImagesProcessor.combine(
        baseImagesFolderPath="./labs/lab_1/input",
        transformedFoldersPaths=[
            "./labs/lab_1/output",
        ],
        outputFolderPath="./labs/lab_1/output/combined",
    )

    ImagesProcessor.addImagesToReadme(
        inputFolderPath="./labs/lab_1/output/combined",
        outputPath="./labs/lab_1",
        relativePathFromOutputToInput="./output/combined",
    )


def lab2():
    grayscaleProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_2/input",
        outputFolderPath="./labs/lab_2/output/grayscale",
        supportImageTypes=["png"],
    )

    grayscaleTransformers = [
        GrayscaleTransformer(grayFromRGB=GrayscaleTransformer.photoshopGrayColor),
        GrayscaleTransformer(grayFromRGB=GrayscaleTransformer.avgGrayColor),
    ]

    globalBinarzationProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_2/output/grayscale",
        outputFolderPath="./labs/lab_2/output/global",
        supportImageTypes=["png"],
    )

    globalBinarzationTransformers = [
        GlobalBinzrizationTransformer(threshold=64),
        GlobalBinzrizationTransformer(threshold=128),
        GlobalBinzrizationTransformer(threshold=192),
    ]

    binarizationProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_2/output/grayscale",
        outputFolderPath="./labs/lab_2/output/binarization",
        supportImageTypes=["png"],
    )

    binarizationTransformers = [
        HistogramBinarizationTransformer(bins=30, threshold=100),
        HistogramBinarizationTransformer(bins=255, threshold=1500),
        HistogramBinarizationTransformer(bins=256, threshold=100),
    ]

    # grayscaleProcessor.transformByAll(grayscaleTransformers)
    binarizationProcessor.transformByAll(binarizationTransformers)
    globalBinarzationProcessor.transformByAll(globalBinarzationTransformers)

    ImagesProcessor.combine(
        baseImagesFolderPath="./labs/lab_2/input",
        transformedFoldersPaths=[
            "./labs/lab_2/output/grayscale",
            "./labs/lab_2/output/global",
            "./labs/lab_2/output/binarization",
        ],
        outputFolderPath="./labs/lab_2/output/combined",
    )

    ImagesProcessor.addImagesToReadme(
        inputFolderPath="./labs/lab_2/output/combined",
        outputPath="./labs/lab_2",
        relativePathFromOutputToInput="./output/combined",
    )


def lab3():
    openingProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_3/input",
        outputFolderPath="./labs/lab_3/output/opening",
        supportImageTypes=["png"],
    )

    openingTransformers = [
        MorphologicalOpeningTransformer(
            isWhite=False,
            aperture=[
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ],
        ),
        MorphologicalOpeningTransformer(
            isWhite=True,
            aperture=[
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ],
        ),
    ]

    # openingProcessor.transformByAll(openingTransformers)

    ImagesProcessor.xorImages(
        baseImagesFolderPath="./labs/lab_3/input",
        toXorFolderPath="./labs/lab_3/output/opening",
        outputFolderPath="./labs/lab_3/output/xor",
    )

    ImagesProcessor.combine(
        baseImagesFolderPath="./labs/lab_3/input",
        transformedFoldersPaths=[
            "./labs/lab_3/output/opening",
            "./labs/lab_3/output/xor",
        ],
        outputFolderPath="./labs/lab_3/output/combined",
    )

    ImagesProcessor.addImagesToReadme(
        inputFolderPath="./labs/lab_3/output/combined",
        outputPath="./labs/lab_3",
        relativePathFromOutputToInput="./output/combined",
    )


def lab4():
    outlineProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_4/input",
        outputFolderPath="./labs/lab_4/output/outline",
        supportImageTypes=["png"],
    )

    outlineTransformers = [
        OutlineRobertsTransformer(matrix="Gx"),
        OutlineRobertsTransformer(matrix="Gy"),
        OutlineRobertsTransformer(matrix="G"),
    ]

    # outlineProcessor.transformByAll(outlineTransformers)

    binarizationProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_4/output/outline",
        outputFolderPath="./labs/lab_4/output/binarization",
        supportImageTypes=["png"],
        filter="_G.",
    )

    binarizationTransformers = [
        GlobalBinzrizationTransformer(threshold=64),
    ]

    binarizationProcessor.transformByAll(binarizationTransformers)

    ImagesProcessor.combine(
        baseImagesFolderPath="./labs/lab_4/input",
        transformedFoldersPaths=[
            "./labs/lab_4/output/outline",
            "./labs/lab_4/output/binarization",
        ],
        outputFolderPath="./labs/lab_4/output/combined",
    )

    ImagesProcessor.addImagesToReadme(
        inputFolderPath="./labs/lab_4/output/combined",
        outputPath="./labs/lab_4",
        relativePathFromOutputToInput="./output/combined",
    )


def lab5():
    CSV_PATH = "./labs/lab_5/output/data.csv"
    COMBINED_PATH = "./labs/lab_5/output/combined"
    FIGURES_PATH = "./labs/lab_5/output/figures"
    INPUT_PATH = "./labs/lab_5/input"

    letters1 = ["א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י"]
    letters2 = ["כ", "ך", "מ", "ם", "נ", "ן", "ס", "ע"]
    letters3 = ["פ", "ף", "צ", "ץ", "ק", "ר", "ש", "ת", "ל"]
    letters = letters1 + letters2 + letters3

    generator = LettersImageGenerator(
        outputPath=INPUT_PATH,
        fontPath="./fonts/arial.ttf",
        letters=letters,
    )

    # generator.generate()

    lettersPaths = ImagesProcessor.getInputPathsFromFolder(INPUT_PATH)
    for i in range(len(lettersPaths)):
        info = ImageInfo(
            inputPath=lettersPaths[i],
        )

        if i == 0:
            info.createCsv(outputCsvPath=CSV_PATH)

        info.printInfo()
        info.saveProfileImages(path=FIGURES_PATH)
        info.exportCsv(letter=letters[i], path=CSV_PATH)

    ImagesProcessor.combine(
        baseImagesFolderPath=INPUT_PATH,
        transformedFoldersPaths=[
            FIGURES_PATH,
        ],
        outputFolderPath=COMBINED_PATH,
        color=(255, 255, 255),
        printFilename=False,
    )

    ImagesProcessor.addImagesToReadme(
        inputFolderPath=COMBINED_PATH,
        outputPath="./labs/lab_5",
        relativePathFromOutputToInput="./output/combined",
    )


def main():
    # lab1()
    # lab2()
    # lab3()
    # lab4()
    lab5()


if __name__ == "__main__":
    main()
