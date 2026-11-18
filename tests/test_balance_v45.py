import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v45 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V44 = ROOT / 'experiments/balance-v44/behavior_pack'


class BalanceV45Test(unittest.TestCase):
    def test_preserves_vanilla_buried_ore_above_minus20(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v45')
            self.assertFalse((pack / 'features/diamond_ore_buried_feature.json').exists())
            scan = json.loads((pack / 'features/scan_chunk.json').read_text())
            distribution = scan['minecraft:scatter_feature']['distribution']
            self.assertEqual(distribution['y']['extent'], [0, 44])
            self.assertEqual(distribution['iterations'], 16 * 16 * 45)
            thin = json.loads((pack / 'feature_rules/thin_overworld.json').read_text())
            self.assertEqual(thin['minecraft:feature_rules']['distribution']['y'], -64)
            for name in ('cave_rule', 'cave_mid_rule', 'cave_upper_rule'):
                self.assertEqual((pack / f'feature_rules/{name}.json').read_bytes(),
                                 (V44 / f'feature_rules/{name}.json').read_bytes())
            self.assertEqual((pack / 'features/thin_diamond.json').read_bytes(),
                             (V44 / 'features/thin_diamond.json').read_bytes())
            self.assertEqual((pack / 'features/thin_deepslate.json').read_bytes(),
                             (V44 / 'features/thin_deepslate.json').read_bytes())

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
