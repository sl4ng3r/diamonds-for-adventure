import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v38 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V37 = ROOT / 'experiments/balance-v37/behavior_pack'
REMOVED = Path('feature_rules/cave_deep_extra2.json')


class BalanceV38Test(unittest.TestCase):
    def test_removes_only_the_narrow_deep_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v38')
            old = {p.relative_to(V37): p.read_bytes() for p in V37.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old) - set(new), {REMOVED})
            self.assertEqual(set(new) - set(old), set())
            self.assertEqual({name for name in new if old[name] != new[name]},
                             {Path('manifest.json')})
            self.assertEqual(old[Path('feature_rules/cave_upper_rule.json')],
                             new[Path('feature_rules/cave_upper_rule.json')])
            manifest = json.loads(new[Path('manifest.json')])
            self.assertIn('V38', manifest['header']['name'])

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
