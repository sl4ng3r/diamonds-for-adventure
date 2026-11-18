import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v43 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V42 = ROOT / 'experiments/balance-v42/behavior_pack'


class BalanceV43Test(unittest.TestCase):
    def test_only_eligible_buried_thinning_becomes_certain(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v43')
            old = {p.relative_to(V42): p.read_bytes() for p in V42.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('manifest.json'), Path('features/thin_diamond.json'),
                              Path('features/thin_deepslate.json')})
            for name, host in (('thin_diamond', 'minecraft:stone'),
                               ('thin_deepslate', 'minecraft:deepslate')):
                path = Path(f'features/{name}.json')
                before = json.loads(old[path])
                after = json.loads(new[path])
                self.assertEqual(after['minecraft:single_block_feature']['places_block'], host)
                after['minecraft:single_block_feature']['places_block'] = before['minecraft:single_block_feature']['places_block']
                self.assertEqual(after, before)
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
