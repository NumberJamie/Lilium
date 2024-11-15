import unittest

from lilium.hasher import ImageHasher


class TestImageHasher(unittest.TestCase):
    hasher = ImageHasher(size=4)

    def test_mean(self):
        self.hasher.size = 2
        self.assertEqual(self.hasher.mean([[10, 20], [30, 40]]), 25)

    def test_transpose(self):
        self.assertEqual(self.hasher.transpose([[1, 2, 3]]), [[1], [2], [3]])
        self.assertEqual(self.hasher.transpose([[1, 2], [3, 4]]), [[1, 3], [2, 4]])

    def test_low_frequency(self):
        self.assertEqual(self.hasher.low_frequency([[1, 2, 3, 4] for _ in range(4)]), [[1]])


if __name__ == '__main__':
    unittest.main()
