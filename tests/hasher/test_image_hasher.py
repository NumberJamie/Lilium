import math
import unittest

from lilium.hasher import ImageHasher


class TestImageHasher(unittest.TestCase):
    image_hasher = ImageHasher(size=4)
    test_data = [[143, 128, 74, 193], [190, 185, 77, 100], [43, 209, 45, 84], [79, 159, 141, 102]]

    def recursive_is_close(self, expected: list[list|float], data: list[list|float]):
        for index, value in enumerate(data):
            if isinstance(value, list):
                self.recursive_is_close(expected[index], value)
                return
            self.assertTrue(math.isclose(expected[index], value), f'Expected: {expected[index]}, Got: {value}.')

    def test_get_mean(self):
        self.assertEqual(self.image_hasher.get_mean(self.test_data), 244)

    def test_transpose(self):
        input_data = [[0, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        expected = [[0, 5, 9, 13], [1, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]]
        self.assertEqual(self.image_hasher.transpose(input_data), expected)

    def test_dct(self):
        expected = [[269.0, -18.051779417962095, 66.99999999999999, -48.80710255531709],
                    [276.0, 88.01992282733157, 13.999999999999996, -46.20057559674545],
                    [190.49999999999997, 17.59353943202244, -63.499999999999986, -118.2326831728599],
                    [240.5, -10.154709194762555, -59.49999999999999, -17.98282183556865]]
        for index, pixels in enumerate(self.test_data):
            pixel_dct = self.image_hasher.dct(pixels)
            self.recursive_is_close(expected[index], pixel_dct)

    def test_apply_dct(self):
        expected = [[487.99999999999994, 38.70348682331468, -20.999999999999996, -115.61159158024554],
                    [41.75465553073829, 13.898232278140824, 103.61145640909591, -0.6451839509358841],
                    [21.499999999999996, -66.90997543603932, 28.499999999999986, 48.82166718935979],
                    [-48.14352232138181, -48.14518395093587, -16.398661554712632, -55.398232278140824]]
        image_data = self.image_hasher.apply_dct(self.test_data)
        self.recursive_is_close(expected, image_data)

if __name__ == '__main__':
    unittest.main()
