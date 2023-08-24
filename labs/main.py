from images_processor import ImagesProcessor
from lab_1.src.transformers import *
from lab_2.src.transformers import (
    GrayscaleTransformer,
    HistogramBinarizationTransformer,
)


def lab1():
    processor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_1/input",
        outputFolderPath="./labs/lab_1/output",
        combinedFolderPath="./labs/lab_1/output/Combined",
        markdownFilePath="./labs/lab_1/README.md",
        markdownImagesFolderPath="./output/Combined",
        supportImageTypes=["png"],
    )

    transformers = [
        UpsamplingTransformer(M=2),
        DownsamplingTransformer(N=4),
        ResamplingTransformer1Pass(M=2, N=4),
        ResamplingTransformer2Pass(M=2, N=4),
    ]

    processor.transformByAll(transformers)
    processor.combine(transformers)
    processor.addCombinedtoReadme()


def lab2():
    grayscaleProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_2/input",
        outputFolderPath="./labs/lab_2/output",
        combinedFolderPath="./labs/lab_2/output/Combined",
        markdownFilePath="./labs/lab_2/README.md",
        markdownImagesFolderPath="./output/Combined",
        supportImageTypes=["png"],
    )

    binarizationProcessor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./labs/lab_2/output/GrayscaleTransformerAvg",
        outputFolderPath="./labs/lab_2/output",
        combinedFolderPath="./labs/lab_2/output/Combined",
        markdownFilePath="./labs/lab_2/README.md",
        markdownImagesFolderPath="./output/Combined",
        supportImageTypes=["png"],
    )

    grayscaleTransformers = [
        GrayscaleTransformer(grayFromRGB=GrayscaleTransformer.photoshopGrayColor),
        GrayscaleTransformer(grayFromRGB=GrayscaleTransformer.avgGrayColor),
    ]

    binarizationTransformers = [
        # HistogramBinarizationTransformer(bins=5, threshold=10),
        # HistogramBinarizationTransformer(bins=8),
        # HistogramBinarizationTransformer(bins=10),
        # HistogramBinarizationTransformer(bins=15),
        # HistogramBinarizationTransformer(bins=30, threshold=100),
        HistogramBinarizationTransformer(bins=255, threshold=1500),
        # HistogramBinarizationTransformer(bins=256, threshold=100),
    ]

    # grayscaleProcessor.transformByAll(grayscaleTransformers)
    # grayscaleProcessor.combine(grayscaleTransformers)
    # grayscaleProcessor.addCombinedtoReadme()

    binarizationProcessor.transformByAll(binarizationTransformers)
    binarizationProcessor.combine()
    binarizationProcessor.addCombinedtoReadme()


def main():
    # lab1()
    lab2()


if __name__ == "__main__":
    main()
