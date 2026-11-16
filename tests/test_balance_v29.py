import json
import unittest
import zipfile
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
V28=ROOT/'experiments/balance-v28/behavior_pack'
V29=ROOT/'experiments/balance-v29/behavior_pack'


class BalanceV29Test(unittest.TestCase):
    def test_only_upper_height_and_chance_change(self):
        old={p.relative_to(V28):p.read_bytes() for p in V28.rglob('*') if p.is_file()}
        new={p.relative_to(V29):p.read_bytes() for p in V29.rglob('*') if p.is_file()}
        self.assertEqual(set(old),set(new))
        self.assertEqual({name for name in old if old[name]!=new[name]},
                         {Path('manifest.json'),Path('feature_rules/cave_upper_rule.json'),
                          Path('features/cave_upper_chance.json')})
        rule=json.loads(new[Path('feature_rules/cave_upper_rule.json')])['minecraft:feature_rules']
        self.assertEqual(rule['distribution']['y']['extent'],[12,26])
        self.assertEqual(rule['description']['places_feature'],'cavediamonds:cave_upper_chance')
        chance=json.loads(new[Path('features/cave_upper_chance.json')])['minecraft:scatter_feature']
        self.assertEqual(chance['distribution']['scatter_chance'],10)
        for surface in ('floor','ceiling','wall'):
            feature=json.loads(new[Path(f'features/cave_snap_{surface}_upper.json')])['minecraft:snap_to_surface_feature']
            self.assertEqual(feature['search_range'],4)

    def test_archive_matches_source(self):
        archive=ROOT/'experiments/balance-v29/cave-diamonds-v29-upper30-test.mcpack'
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            files={p.relative_to(V29).as_posix():p.read_bytes() for p in V29.rglob('*') if p.is_file()}
            self.assertEqual(set(z.namelist()),set(files))
            for name,content in files.items():
                self.assertEqual(z.read(name),content)
