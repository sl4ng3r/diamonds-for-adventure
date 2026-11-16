import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v32 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V30 = ROOT / 'experiments/balance-v30/behavior_pack'
V32 = ROOT / 'experiments/balance-v32/behavior_pack'


class BalanceV32Test(unittest.TestCase):
    def test_only_wrapper_chance_changes(self):
        old = {p.relative_to(V30): p.read_bytes() for p in V30.rglob('*') if p.is_file()}
        new = {p.relative_to(V32): p.read_bytes() for p in V32.rglob('*') if p.is_file()}
        self.assertEqual(set(old), set(new))
        self.assertEqual({name for name in old if old[name] != new[name]},
                         {Path('manifest.json'), Path('features/cave_regular_chance.json')})
        old_wrapper = json.loads(old[Path('features/cave_regular_chance.json')])
        new_wrapper = json.loads(new[Path('features/cave_regular_chance.json')])
        old_wrapper['minecraft:scatter_feature']['distribution']['scatter_chance'] = 30
        self.assertEqual(new_wrapper, old_wrapper)

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
