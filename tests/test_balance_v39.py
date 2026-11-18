import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v39 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V37 = ROOT / 'experiments/balance-v37/behavior_pack'
DEEP_RULE = Path('feature_rules/cave_deep_extra2.json')


class BalanceV39Test(unittest.TestCase):
    def test_only_narrow_deep_chance_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v39')
            old = {p.relative_to(V37): p.read_bytes() for p in V37.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('manifest.json'), DEEP_RULE})
            old_rule = json.loads(old[DEEP_RULE])
            new_rule = json.loads(new[DEEP_RULE])
            self.assertEqual(old_rule['minecraft:feature_rules']['distribution']['scatter_chance'], 40)
            self.assertEqual(new_rule['minecraft:feature_rules']['distribution']['scatter_chance'], 30)
            new_rule['minecraft:feature_rules']['distribution']['scatter_chance'] = 40
            self.assertEqual(new_rule, old_rule)
            self.assertEqual(new[Path('feature_rules/cave_upper_rule.json')],
                             old[Path('feature_rules/cave_upper_rule.json')])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
