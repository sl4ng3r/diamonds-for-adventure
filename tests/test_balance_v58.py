import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v58 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V57 = ROOT / 'experiments/balance-v57/behavior_pack'


class BalanceV58Test(unittest.TestCase):
    def test_adds_only_small_upper_middle_cave_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v58')
            old = {p.relative_to(V57): p.read_bytes() for p in V57.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            extra = Path('feature_rules/cave_mid_upper_rule.json')
            self.assertEqual(set(new), set(old) | {extra})
            self.assertEqual({name for name in old if old[name] != new[name]}, {Path('manifest.json')})
            lower = json.loads(new[Path('feature_rules/cave_mid_rule.json')])['minecraft:feature_rules']
            upper = json.loads(new[extra])['minecraft:feature_rules']
            self.assertEqual(lower['distribution']['y']['extent'], [-32, -17])
            self.assertEqual(lower['distribution']['scatter_chance'], 8)
            self.assertEqual(upper['description']['identifier'], 'cavediamonds:cave_mid_upper_rule')
            self.assertEqual(upper['description']['places_feature'], lower['description']['places_feature'])
            self.assertEqual(upper['distribution']['y']['extent'], [-16, -1])
            self.assertEqual(upper['distribution']['scatter_chance'], 4)

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
