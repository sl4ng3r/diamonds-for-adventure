import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v48 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V47 = ROOT / 'experiments/balance-v47/behavior_pack'


class BalanceV48Test(unittest.TestCase):
    def test_makes_upper_buried_veins_larger_and_less_frequent(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v48')
            old = {p.relative_to(V47): p.read_bytes() for p in V47.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('features/sparse_buried.json'),
                              Path('feature_rules/upper_buried_rule.json'), Path('manifest.json')})
            feature = json.loads(new[Path('features/sparse_buried.json')])
            rule = json.loads(new[Path('feature_rules/upper_buried_rule.json')])
            self.assertEqual(feature['minecraft:ore_feature']['count'], 8)
            self.assertEqual(rule['minecraft:feature_rules']['distribution']['scatter_chance'], 65)
            self.assertEqual(rule['minecraft:feature_rules']['distribution']['y']['extent'], [-19, 16])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
