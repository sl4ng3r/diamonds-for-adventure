import json
import unittest
import zipfile
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
V27=ROOT/'experiments/balance-v27/behavior_pack'
V28=ROOT/'experiments/balance-v28/behavior_pack'


class BalanceV28Test(unittest.TestCase):
    def test_only_upper_rule_is_throttled(self):
        old={p.relative_to(V27):p.read_bytes() for p in V27.rglob('*') if p.is_file()}
        new={p.relative_to(V28):p.read_bytes() for p in V28.rglob('*') if p.is_file()}
        self.assertEqual(set(old)-set(new),set())
        self.assertEqual(set(new)-set(old),{Path('features/cave_upper_chance.json')})
        self.assertEqual({name for name in old.keys() & new.keys() if old[name]!=new[name]},
                         {Path('manifest.json'),Path('feature_rules/cave_upper_rule.json')})
        rule=json.loads(new[Path('feature_rules/cave_upper_rule.json')])['minecraft:feature_rules']
        self.assertEqual(rule['description']['places_feature'],'cavediamonds:cave_upper_chance')
        chance=json.loads(new[Path('features/cave_upper_chance.json')])['minecraft:scatter_feature']
        self.assertEqual(chance['places_feature'],'cavediamonds:cave_snap_choice_upper')
        self.assertEqual(chance['distribution'],{'iterations':1,'scatter_chance':20,'x':0,'y':0,'z':0})

    def test_test_archive_matches_pack(self):
        path=ROOT/'experiments/balance-v28/cave-diamonds-v28-upper25-test.mcpack'
        with zipfile.ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            files={p.relative_to(V28).as_posix():p.read_bytes() for p in V28.rglob('*') if p.is_file()}
            self.assertEqual(set(z.namelist()),set(files))
            for name,content in files.items():
                self.assertEqual(z.read(name),content)
