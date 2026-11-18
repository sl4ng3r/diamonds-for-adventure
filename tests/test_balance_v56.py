import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v56 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V55 = ROOT / 'experiments/balance-v55/behavior_pack'
V51 = ROOT / 'experiments/balance-v51/behavior_pack'


class BalanceV56Test(unittest.TestCase):
    def test_cave_and_deep_rules_match_the_previous_fixed_version(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v56')
            for name in ('cave_rule', 'cave_mid_rule', 'cave_upper_rule', 'thin_overworld'):
                relative = Path('feature_rules') / f'{name}.json'
                self.assertEqual((pack / relative).read_bytes(), (V51 / relative).read_bytes())

    def test_increases_only_upper_thinning_weight(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'v56')
            old = {p.relative_to(V55): p.read_bytes() for p in V55.rglob('*') if p.is_file()}
            new = {p.relative_to(pack): p.read_bytes() for p in pack.rglob('*') if p.is_file()}
            self.assertEqual(set(old), set(new))
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('features/thin_upper_diamond.json'),
                              Path('features/thin_upper_deepslate.json'), Path('manifest.json')})
            for name in ('diamond', 'deepslate'):
                feature = json.loads(new[Path(f'features/thin_upper_{name}.json')])
                blocks = feature['minecraft:single_block_feature']['places_block']
                self.assertEqual([block['weight'] for block in blocks], [2, 1])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
