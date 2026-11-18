import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v44 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V43 = ROOT / 'experiments/balance-v43/behavior_pack'
V37 = ROOT / 'experiments/balance-v37/behavior_pack'


class BalanceV44Test(unittest.TestCase):
    def test_adds_two_sparse_cave_rules_to_preserved_vanilla_veins(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v44')
            old = {p.relative_to(V43): p.read_bytes() for p in V43.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            added = {Path('feature_rules/cave_rule.json'),
                     Path('feature_rules/cave_mid_rule.json')}
            self.assertEqual(set(old) - set(new), set())
            self.assertEqual(set(new) - set(old), added)
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('manifest.json')})
            for name, chance in (('cave_rule', 10), ('cave_mid_rule', 15)):
                path = Path(f'feature_rules/{name}.json')
                source = json.loads((V37 / path).read_text())
                actual = json.loads(new[path])
                self.assertEqual(actual['minecraft:feature_rules']['distribution']['scatter_chance'], chance)
                if name == 'cave_rule':
                    actual['minecraft:feature_rules']['distribution'].pop('scatter_chance')
                else:
                    actual['minecraft:feature_rules']['distribution']['scatter_chance'] = 90
                self.assertEqual(actual, source)
            self.assertNotIn(Path('feature_rules/cave_deep_extra.json'), new)
            self.assertNotIn(Path('feature_rules/cave_deep_extra2.json'), new)
            for name in ('feature_rules/cave_upper_rule.json',
                         'feature_rules/thin_overworld.json'):
                self.assertEqual(new[Path(name)], old[Path(name)])

    def test_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__ == '__main__':
    unittest.main()
