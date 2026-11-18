import unittest

from tools.cave_spatial_compare import compare_exposed_positions, measure_scan


def ore(x, y, z, air=False):
    neighbours = ['minecraft:deepslate'] * 6
    if air:
        neighbours[0] = 'minecraft:air'
    return {'x': x, 'y': y, 'z': z,
            'type': 'minecraft:deepslate_diamond_ore', 'neighbours': neighbours}


class CaveSpatialCompareTest(unittest.TestCase):
    def test_counts_sites_once_per_band_and_assigns_one_local_tile(self):
        scan = {'ores': [ore(0, -47, 0, True), ore(0, -48, 0),
                         ore(63, -40, 0, True), ore(64, -40, 0, True),
                         ore(80, -40, 0, True)], 'upperDiamondOre': []}
        result = measure_scan(scan, 0, 0, 64)
        self.assertEqual(result['-47..-32']['groups'], 3)
        self.assertEqual(result['-47..-32']['blocks'], 4)
        self.assertEqual(result['-47..-32']['tiles'], {(0, 0): 2, (1, 0): 1})
        self.assertEqual(result['-64..-48']['groups'], 0)

    def test_group_can_touch_two_height_bands_without_double_counting_total(self):
        scan = {'ores': [ore(1, -48, 1, True), ore(1, -47, 1, True)],
                'upperDiamondOre': []}
        result = measure_scan(scan, 0, 0, 64)
        self.assertEqual(result['-64..-48']['groups'], 1)
        self.assertEqual(result['-47..-32']['groups'], 1)

    def test_rejects_duplicate_ore_positions(self):
        scan = {'ores': [ore(1, -40, 1), ore(1, -40, 1)], 'upperDiamondOre': []}
        with self.assertRaises(ValueError):
            measure_scan(scan, 0, 0, 64)

    def test_reports_lost_and_added_air_exposed_positions(self):
        vanilla = {'ores': [ore(1, -40, 1, True), ore(2, -40, 1, True)]}
        candidate = {'ores': [ore(1, -40, 1, True), ore(3, -40, 1, True)],
                     'upperDiamondOre': [ore(4, 20, 1, True)]}
        self.assertEqual(compare_exposed_positions(vanilla, candidate),
                         {'vanilla': 2, 'candidate': 3, 'retained': 1,
                          'lost': 1, 'added': 2})


if __name__ == '__main__':
    unittest.main()
