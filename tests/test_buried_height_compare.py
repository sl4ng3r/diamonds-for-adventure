import unittest

from tools.buried_height_compare import buried_metrics


def ore(x, y, z, neighbours=None):
    return {'x': x, 'y': y, 'z': z,
            'neighbours': neighbours or ['minecraft:stone'] * 6}


class BuriedHeightCompareTest(unittest.TestCase):
    def test_counts_connected_buried_sites_only_above_minus20(self):
        ores = [ore(0, -19, 0), ore(1, -19, 0), ore(1, -20, 0),
                ore(8, 0, 0), ore(10, 0, 0, ['minecraft:air'] + ['minecraft:stone'] * 5),
                ore(11, 0, 0, ['minecraft:water'] + ['minecraft:stone'] * 5)]
        self.assertEqual(buried_metrics(ores), {'blocks': 3, 'groups': 2,
                                                 'positions': {(0, -19, 0), (1, -19, 0), (8, 0, 0)}})


if __name__ == '__main__':
    unittest.main()
