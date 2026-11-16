import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v33 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V32 = ROOT / 'experiments/balance-v32/behavior_pack'
V33 = ROOT / 'experiments/balance-v33/behavior_pack'


class BalanceV33Test(unittest.TestCase):
    def test_deep_and_mid_chances_are_separate(self):
        old = {p.relative_to(V32): p.read_bytes() for p in V32.rglob('*') if p.is_file()}
        new = {p.relative_to(V33): p.read_bytes() for p in V33.rglob('*') if p.is_file()}
        self.assertEqual(set(old) - set(new), {Path('features/cave_regular_chance.json')})
        self.assertEqual(set(new) - set(old),
                         {Path('features/cave_deep_chance.json'),
                          Path('features/cave_mid_chance.json')})
        self.assertEqual({name for name in old if name in new and old[name] != new[name]},
                         {Path('manifest.json')} |
                         {Path(f'feature_rules/{name}.json') for name in
                          ('cave_rule','cave_deep_extra','cave_deep_extra2','cave_mid_rule')})
        for name,chance in (('deep',20),('mid',60)):
            wrapper = json.loads(new[Path(f'features/cave_{name}_chance.json')])['minecraft:scatter_feature']
            self.assertEqual(wrapper['distribution']['scatter_chance'],chance)
            self.assertEqual(wrapper['places_feature'],'cavediamonds:cave_snap_choice')
        for name in ('cave_rule','cave_deep_extra','cave_deep_extra2'):
            rule=json.loads(new[Path(f'feature_rules/{name}.json')])['minecraft:feature_rules']
            self.assertEqual(rule['description']['places_feature'],'cavediamonds:cave_deep_chance')
        mid=json.loads(new[Path('feature_rules/cave_mid_rule.json')])['minecraft:feature_rules']
        self.assertEqual(mid['description']['places_feature'],'cavediamonds:cave_mid_chance')

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
