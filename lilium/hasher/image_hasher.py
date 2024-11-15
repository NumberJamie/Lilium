import math

from pyvips import Image

from lilium.types import ImageData


class ImageHasher:
    def __init__(self, size: int = 32):
        self.size = size
        self.colorspace = 'b-w'

    @staticmethod
    def transpose(image_data: ImageData) -> ImageData:
        return [list(pixels) for pixels in zip(*image_data)]

    def mean(self, image_data: ImageData) -> int:
        total = 0
        for pixels in image_data:
            total += sum(pixels)
        return total // (self.size * 2)

    def hash(self, path: str) -> hex:
        hash_value = 0
        image_data = self.apply_dct(self.get_data(path))
        low_frequency = self.low_frequency(image_data)
        mean = self.mean(low_frequency)
        for column in low_frequency:
            for pixel in column:
                hash_value = (hash_value << 1) | (0 if pixel < mean else 1)
        return hex(hash_value)[2:]

    def get_data(self, path: str) -> ImageData:
        image = Image.thumbnail(path, self.size, height=self.size, size='force').colourspace(self.colorspace)
        return image.flatten().tolist()

    def low_frequency(self, image_data: ImageData) -> ImageData:
        dct_slice = int(self.size / 4)
        return [image_data[index][:dct_slice] for index in range(dct_slice)]

    def apply_dct(self, image_data: ImageData) -> ImageData:
        dct_image_data = [self.dct(pixels) for pixels in image_data]
        dct_image_data = self.transpose(dct_image_data)
        dct_image_data = [self.dct(pixels) for pixels in dct_image_data]
        return self.transpose(dct_image_data)

    def dct(self, pixels: list[float]) -> list[float]:
        pixels_dct = []
        factor = math.pi / (2 * self.size)
        for index in range(self.size):
            total = 0.0
            for pixel in range(self.size):
                total += pixels[pixel] * math.cos((2 * pixel + 1) * index * factor)
            scale = math.sqrt(1 / self.size) if index == 0 else math.sqrt(2 / self.size)
            pixels_dct.append(total * scale)
        return pixels_dct
