import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v30 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V29 = ROOT / 'experiments/balance-v29/behavior_pack'
V30 = ROOT / 'experiments/balance-v30/behavior_pack'
RULES = ('cave_rule', 'cave_mid_rule', 'cave_deep_extra', 'cave_deep_extra2')


class BalanceV30Test(unittest.TestCase):
    def test_only_regular_cave_rule_wrappers_change(self):
        old = {p.relative_to(V29): p.read_bytes() for p in V29.rglob('*') if p.is_file()}
        new = {p.relative_to(V30): p.read_bytes() for p in V30.rglob('*') if p.is_file()}
        self.assertEqual(set(new) - set(old), {Path('features/cave_regular_chance.json')})
        self.assertEqual(set(old) - set(new), set())
        self.assertEqual(
            {name for name in old if old[name] != new[name]},
            {Path('manifest.json')} | {Path(f'feature_rules/{name}.json') for name in RULES},
        )
        wrapper = json.loads(new[Path('features/cave_regular_chance.json')])['minecraft:scatter_feature']
        self.assertEqual(wrapper['distribution']['scatter_chance'], 45)
        self.assertEqual(wrapper['places_feature'], 'cavediamonds:cave_snap_choice')
        for rule_name in RULES:
            old_rule = json.loads(old[Path(f'feature_rules/{rule_name}.json')])
            new_rule = json.loads(new[Path(f'feature_rules/{rule_name}.json')])
            old_rule['minecraft:feature_rules']['description']['places_feature'] = (
                'cavediamonds:cave_regular_chance'
            )
            self.assertEqual(new_rule, old_rule)

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
