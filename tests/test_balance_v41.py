import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v41 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V37 = ROOT / 'experiments/balance-v37/behavior_pack'
REMOVED = {Path(f'features/diamond_ore_{kind}feature.json') for kind in ('', 'large_')} | {
    Path(f'feature_rules/{name}.json') for name in
    ('cave_rule', 'cave_deep_extra', 'cave_deep_extra2', 'cave_mid_rule', 'sparse_buried_rule')
}


class BalanceV41Test(unittest.TestCase):
    def test_preserves_vanilla_normal_and_large_features_and_upper_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v41')
            old = {p.relative_to(V37): p.read_bytes() for p in V37.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old) - set(new), REMOVED)
            self.assertEqual(set(new) - set(old), set())
            self.assertEqual({name for name in new if old[name] != new[name]},
                             {Path('manifest.json')})
            self.assertEqual(new[Path('feature_rules/cave_upper_rule.json')],
                             old[Path('feature_rules/cave_upper_rule.json')])
            self.assertEqual(new[Path('features/diamond_ore_buried_feature.json')],
                             old[Path('features/diamond_ore_buried_feature.json')])
            self.assertIn('V41', json.loads(new[Path('manifest.json')])['header']['name'])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
