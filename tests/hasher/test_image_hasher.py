import math
import unittest

from lilium.hasher import ImageHasher


class TestImageHasher(unittest.TestCase):
    hasher = ImageHasher(size=2)

    def recursive_is_close(self, answer: list[list|float], expected: list[list|float]):
        for index, value in enumerate(answer):
            if isinstance(value, list):
                self.recursive_is_close(value, expected[index])
                continue
            self.assertTrue(math.isclose(int(value), expected[index]), f'Expected: {expected[index]}, Got: {value}')

    def test_image_hasher(self):
        self.assertEqual(self.hasher.size, 2)
        self.assertEqual(self.hasher.colorspace, 'b-w')

    def test_get_data(self):
        self.assertRaises(FileNotFoundError, self.hasher.get_data, './image.png')
        self.assertEqual(self.hasher.get_data('./test_image.png'), [[255, 127], [127, 0]])

    def test_dct(self):
        test_data = [[10, 20], [30, 40]]
        expected = [[21, -7], [49, -7]]
        for index, value in enumerate(test_data):
            self.recursive_is_close(self.hasher.dct(value), expected[index])

    def test_apply_dct(self):
        self.recursive_is_close(self.hasher.apply_dct([[10, 20], [30, 40]]), [[50, -10], [-20, 0]])

    def test_mean(self):
        self.assertEqual(self.hasher.mean([[10, 20], [30, 40]]), 25)

    def test_transpose(self):
        self.assertEqual(self.hasher.transpose([[1, 2, 3]]), [[1], [2], [3]])
        self.assertEqual(self.hasher.transpose([[1, 2], [3, 4]]), [[1, 3], [2, 4]])

    def test_low_frequency(self):
        self.hasher.size = 4
        self.assertEqual(self.hasher.low_frequency([[1, 2, 3, 4] for _ in range(4)]), [[1]])
        self.hasher.size = 2
        self.assertEqual(self.hasher.low_frequency([[1, 2, 3, 4] for _ in range(4)]), [])


if __name__ == '__main__':
    unittest.main()
