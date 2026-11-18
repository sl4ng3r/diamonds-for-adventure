import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v50 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V49 = ROOT / 'experiments/balance-v49/behavior_pack'


class BalanceV50Test(unittest.TestCase):
    def test_tunes_only_upper_buried_frequency(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v50')
            old = {p.relative_to(V49): p.read_bytes() for p in V49.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('feature_rules/upper_buried_rule.json'), Path('manifest.json')})
            rule = json.loads(new[Path('feature_rules/upper_buried_rule.json')])
            self.assertEqual(rule['minecraft:feature_rules']['distribution']['scatter_chance'], 50)

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
