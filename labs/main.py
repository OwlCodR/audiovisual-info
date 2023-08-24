from images_processor import ImagesProcessor
from lab_1.src.transformers import *
from lab_2.src.transformers import (
    GrayscaleTransformer,
    HistogramBinarizationTransformer,
)
from lab_3.src.transformers import MorphologicalOpeningTransformer


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
    # binarizationProcessor.transformByAll(binarizationTransformers)

    ImagesProcessor.combine(
        baseImagesFolderPath="./labs/lab_2/input",
        transformedFoldersPaths=[
            "./labs/lab_2/output/grayscale",
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


def main():
    # lab1()
    # lab2()
    lab3()


if __name__ == "__main__":
    main()
