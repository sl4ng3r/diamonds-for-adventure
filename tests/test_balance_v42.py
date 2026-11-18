import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v42 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V41 = ROOT / 'experiments/balance-v41/behavior_pack'
PROTOTYPE = ROOT / 'prototype/behavior_pack'
THIN_FILES = {Path('feature_rules/thin_overworld.json')} | {
    Path(f'features/{name}.json') for name in
    ('scan_chunk', 'select_ore', 'thin_diamond', 'thin_deepslate')
}


class BalanceV42Test(unittest.TestCase):
    def test_adds_only_late_buried_thinning_to_vanilla_cave_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            target = build_pack(Path(directory) / 'v42')
            old = {p.relative_to(V41): p.read_bytes() for p in V41.rglob('*') if p.is_file()}
            new = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
            self.assertEqual(set(old) - set(new), set())
            self.assertEqual(set(new) - set(old), THIN_FILES)
            self.assertEqual({name for name in old if old[name] != new[name]},
                             {Path('manifest.json')})
            for name in THIN_FILES:
                self.assertEqual(new[name], (PROTOTYPE / name).read_bytes())
            rule = json.loads(new[Path('feature_rules/thin_overworld.json')])
            self.assertEqual(rule['minecraft:feature_rules']['conditions']['placement_pass'], 'final_pass')
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
