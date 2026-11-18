import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v46 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V44 = ROOT / 'experiments/balance-v44/behavior_pack'
V45 = ROOT / 'experiments/balance-v45/behavior_pack'


class BalanceV46Test(unittest.TestCase):
    def test_adds_upper_buried_ore_without_restoring_deep_buried_source(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v46')
            self.assertEqual((pack / 'features/diamond_ore_buried_feature.json').read_bytes(),
                             (V44 / 'features/diamond_ore_buried_feature.json').read_bytes())
            self.assertEqual((pack / 'features/scan_chunk.json').read_bytes(),
                             (V45 / 'features/scan_chunk.json').read_bytes())
            rule = json.loads((pack / 'feature_rules/upper_buried_rule.json').read_text())
            body = rule['minecraft:feature_rules']
            self.assertEqual(body['description']['places_feature'], 'cavediamonds:sparse_buried')
            self.assertEqual(body['conditions']['placement_pass'], 'underground_pass')
            self.assertEqual(body['distribution']['y']['extent'], [-19, 16])
            self.assertEqual(body['distribution']['iterations'], 1)
            for name in ('cave_rule', 'cave_mid_rule', 'cave_upper_rule'):
                self.assertEqual((pack / f'feature_rules/{name}.json').read_bytes(),
                                 (V44 / f'feature_rules/{name}.json').read_bytes())

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
