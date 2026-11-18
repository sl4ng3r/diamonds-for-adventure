import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v47 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V46 = ROOT / 'experiments/balance-v46/behavior_pack'


class BalanceV47Test(unittest.TestCase):
    def test_increases_only_upper_buried_vein_size(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v47')
            old = {p.relative_to(V46): p.read_bytes() for p in V46.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('features/sparse_buried.json'), Path('manifest.json')})
            feature = json.loads(new[Path('features/sparse_buried.json')])
            self.assertEqual(feature['minecraft:ore_feature']['count'], 5)

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
