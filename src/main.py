from images_processor import ImagesProcessor
from lab_1.transformers import *


def lab1():
    processor = ImagesProcessor.fromImagesFolder(
        inputFolderPath=f"./src/lab_1/input",
        outputFolderPath=f"./src/lab_1/output",
        supportImageTypes=["png"],
    )

    interpolationTransformer = InterpolationTransformer(N=2)

    processor.transformImages(interpolationTransformer)


def main():
    lab1()


if __name__ == "__main__":
    main()
