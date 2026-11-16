import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v34 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V33 = ROOT / 'experiments/balance-v33/behavior_pack'
V34 = ROOT / 'experiments/balance-v34/behavior_pack'


class BalanceV34Test(unittest.TestCase):
    def test_only_mid_chance_changes(self):
        old = {p.relative_to(V33): p.read_bytes() for p in V33.rglob('*') if p.is_file()}
        new = {p.relative_to(V34): p.read_bytes() for p in V34.rglob('*') if p.is_file()}
        self.assertEqual(set(old), set(new))
        self.assertEqual({name for name in old if old[name] != new[name]},
                         {Path('manifest.json'), Path('features/cave_mid_chance.json')})
        old_mid = json.loads(old[Path('features/cave_mid_chance.json')])
        new_mid = json.loads(new[Path('features/cave_mid_chance.json')])
        old_mid['minecraft:scatter_feature']['distribution']['scatter_chance'] = 45
        self.assertEqual(new_mid, old_mid)

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
