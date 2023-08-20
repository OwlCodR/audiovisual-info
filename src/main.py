from images_processor import ImagesProcessor
from lab_1.transformers import *


def lab1():
    processor = ImagesProcessor.fromImagesFolder(
        inputFolderPath="./src/lab_1/input",
        outputFolderPath="./src/lab_1/output",
        supportImageTypes=["png"],
    )

    transformers = [
        UpsamplingTransformer(M=2),
        DownsamplingTransformer(N=4),
        ResamplingTransformer1Pass(M=2, N=4),
        ResamplingTransformer2Pass(M=2, N=4),
    ]

    # processor.transformByAll(transformers)
    processor.combine(transformers)


def main():
    lab1()


if __name__ == "__main__":
    main()
