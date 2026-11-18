import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v40 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V37 = ROOT / 'experiments/balance-v37/behavior_pack'
DEEP_RULES = ('cave_rule', 'cave_deep_extra', 'cave_deep_extra2')
FACES = ('floor', 'ceiling', 'wall')


class BalanceV40Test(unittest.TestCase):
    def test_deep_rules_use_shorter_surface_search_only(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v40')
            old = {p.relative_to(V37): p.read_bytes() for p in V37.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old) - set(new), set())
            self.assertEqual(set(new) - set(old),
                             {Path('features/cave_snap_choice_deep.json')} |
                             {Path(f'features/cave_snap_{face}_deep.json') for face in FACES})
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('manifest.json')} |
                             {Path(f'feature_rules/{rule}.json') for rule in DEEP_RULES})
            choice = json.loads(new[Path('features/cave_snap_choice_deep.json')])['minecraft:weighted_random_feature']
            self.assertEqual(choice['features'],
                             [[f'cavediamonds:cave_snap_{face}_deep', 1] for face in FACES])
            for face in FACES:
                source = json.loads(old[Path(f'features/cave_snap_{face}.json')])['minecraft:snap_to_surface_feature']
                deep = json.loads(new[Path(f'features/cave_snap_{face}_deep.json')])['minecraft:snap_to_surface_feature']
                self.assertEqual(deep['search_range'], 6)
                deep['search_range'] = source['search_range']
                deep['description']['identifier'] = source['description']['identifier']
                self.assertEqual(deep, source)
            for rule in DEEP_RULES:
                old_rule = json.loads(old[Path(f'feature_rules/{rule}.json')])
                new_rule = json.loads(new[Path(f'feature_rules/{rule}.json')])
                self.assertEqual(new_rule['minecraft:feature_rules']['description']['places_feature'],
                                 'cavediamonds:cave_snap_choice_deep')
                new_rule['minecraft:feature_rules']['description']['places_feature'] = 'cavediamonds:cave_snap_choice'
                self.assertEqual(new_rule, old_rule)
            self.assertEqual(new[Path('feature_rules/cave_mid_rule.json')],
                             old[Path('feature_rules/cave_mid_rule.json')])
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
