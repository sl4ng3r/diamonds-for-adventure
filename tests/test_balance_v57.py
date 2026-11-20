import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v57 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V56 = ROOT / 'experiments/balance-v56/behavior_pack'


class BalanceV57Test(unittest.TestCase):
    def test_only_mid_cave_start_band_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v57')
            old = {p.relative_to(V56): p.read_bytes() for p in V56.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('feature_rules/cave_mid_rule.json'), Path('manifest.json')})
            rule = json.loads(new[Path('feature_rules/cave_mid_rule.json')])['minecraft:feature_rules']
            self.assertEqual(rule['distribution']['y']['extent'], [-32, -17])
            self.assertEqual(rule['distribution']['scatter_chance'], 8)
            self.assertEqual(new[Path('feature_rules/cave_upper_rule.json')],
                             old[Path('feature_rules/cave_upper_rule.json')])
            self.assertEqual(new[Path('feature_rules/cave_rule.json')],
                             old[Path('feature_rules/cave_rule.json')])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
