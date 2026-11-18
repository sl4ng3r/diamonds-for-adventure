import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v55 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V54 = ROOT / 'experiments/balance-v54/behavior_pack'


class BalanceV55Test(unittest.TestCase):
    def test_adds_partial_upper_thinning_and_keeps_cave_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v55')
            self.assertFalse((pack / 'feature_rules/upper_buried_rule.json').exists())
            self.assertFalse((pack / 'features/sparse_buried.json').exists())
            self.assertEqual((pack / 'features/scan_chunk.json').read_bytes(),
                             (V54 / 'features/scan_chunk.json').read_bytes())
            for name in ('cave_rule', 'cave_mid_rule', 'cave_upper_rule'):
                self.assertEqual((pack / f'feature_rules/{name}.json').read_bytes(),
                                 (V54 / f'feature_rules/{name}.json').read_bytes())
            scan = json.loads((pack / 'features/scan_upper_chunk.json').read_text())
            distribution = scan['minecraft:scatter_feature']['distribution']
            self.assertEqual(distribution['y']['extent'], [0, 35])
            self.assertEqual(distribution['iterations'], 16 * 16 * 36)
            rule = json.loads((pack / 'feature_rules/thin_upper_overworld.json').read_text())
            body = rule['minecraft:feature_rules']
            self.assertEqual(body['conditions']['placement_pass'], 'final_pass')
            self.assertEqual(body['distribution']['y'], -19)
            for name, host, ore in (('diamond', 'minecraft:stone', 'minecraft:diamond_ore'),
                                    ('deepslate', 'minecraft:deepslate', 'minecraft:deepslate_diamond_ore')):
                feature = json.loads((pack / f'features/thin_upper_{name}.json').read_text())
                blocks = feature['minecraft:single_block_feature']['places_block']
                self.assertEqual(blocks, [{'block': host, 'weight': 1}, {'block': ore, 'weight': 2}])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
