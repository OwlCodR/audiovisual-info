from PIL import Image, ImageDraw, ImageFont

import numpy


class LettersImageGenerator:
    def __init__(
        self,
        outputPath: str,
        fontPath: str,
        letters: list[str],
        fontSize=120,
        imgSize=100,
    ) -> None:
        self.__outputPath = outputPath
        self.__fontPath = fontPath
        self.__letters = letters
        self.__fontSize = fontSize
        self.__imgSize = imgSize
    
    def crop(self, img: Image, makeSizeEven=True):
        pixels = numpy.array(img)
        height, width = pixels.shape

        top = height
        left = width
        right = 0
        bottom = 0

        for k in range(height):
            for n in range(width):
                if pixels[k][n] == 0:
                    if k < top:
                        top = k
                    if n < left:
                        left = n
                    if k > bottom:
                        bottom = k
                    if n > right:
                        right = n

        box = (left, top, right, bottom)
        img = img.crop(box)

        if makeSizeEven:
            width, height = img.size

            if height % 2 != 0:
                height += 1

            if width % 2 != 0:
                width += 1

            resized = Image.new("1", (width, height), (1))
            resized.paste(img, (0, 0))
            img = resized
        return img

    def generate(self, crop=True):
        for i in range(len(self.__letters)):
            text = self.__letters[i]

            size = (self.__imgSize, self.__imgSize)
            img = Image.new("1", size, (1))

            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(self.__fontPath, self.__fontSize)
            textX, textY = font.getsize(text)

            draw.text(
                xy=(
                    (self.__imgSize - textX) // 2,
                    (self.__imgSize - textY) // 2 - 16,
                ),
                text=text,
                fill=(0),
                font=font,
            )

            if crop:
                img = self.crop(img)

            img.save(f"{self.__outputPath}/{str(i + 1).zfill(2)}.png")
