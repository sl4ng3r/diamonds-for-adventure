import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v52 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V51 = ROOT / 'experiments/balance-v51/behavior_pack'


class BalanceV52Test(unittest.TestCase):
    def test_reduces_only_upper_buried_frequency(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v52')
            old = {p.relative_to(V51): p.read_bytes() for p in V51.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('feature_rules/upper_buried_rule.json'), Path('manifest.json')})
            rule = json.loads(new[Path('feature_rules/upper_buried_rule.json')])
            distribution = rule['minecraft:feature_rules']['distribution']
            self.assertEqual(distribution['scatter_chance'], 6)
            self.assertEqual(distribution['y']['extent'], [-19, 16])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
