import json
import unittest
import zipfile
from pathlib import Path


ROOT=Path(__file__).resolve().parents[1]
V26=ROOT/'experiments/balance-v26/behavior_pack'
V27=ROOT/'experiments/balance-v27/behavior_pack'


class BalanceV27Test(unittest.TestCase):
    def test_upper_rule_is_only_generation_change_from_v26(self):
        old={p.relative_to(V26):p.read_bytes() for p in V26.rglob('*') if p.is_file()}
        new={p.relative_to(V27):p.read_bytes() for p in V27.rglob('*') if p.is_file()}
        changed={name for name in new.keys() & old.keys() if name!=Path('manifest.json') and new[name]!=old[name]}
        self.assertFalse(changed)
        self.assertEqual(set(old)-set(new),set())
        self.assertEqual(set(new)-set(old),{
            Path('feature_rules/cave_upper_rule.json'),
            *(Path(f'features/cave_snap_{surface}_upper.json') for surface in ('floor','ceiling','wall')),
            Path('features/cave_snap_choice_upper.json')})

    def test_upper_search_and_vein_offsets_have_planned_y25_cap(self):
        rule=json.loads((V27/'feature_rules/cave_upper_rule.json').read_text())['minecraft:feature_rules']
        self.assertEqual(rule['distribution']['y']['extent'],[12,21])
        self.assertEqual(rule['description']['places_feature'],'cavediamonds:cave_snap_choice_upper')
        for surface in ('floor','ceiling','wall'):
            snap=json.loads((V27/f'features/cave_snap_{surface}_upper.json').read_text())['minecraft:snap_to_surface_feature']
            self.assertEqual(snap['search_range'],4)
            self.assertEqual(snap['feature_to_snap'],'cavediamonds:cave_vein_choice')
        for path in V27.glob('features/cave_neighbor_*.json'):
            if path.stem=='cave_neighbor_chance' or path.stem=='cave_neighbor_choice':
                continue
            feature=json.loads(path.read_text())['minecraft:scatter_feature']
            self.assertLessEqual(feature['distribution']['y'],0)

    def test_archive_matches_pack_directory(self):
        archive=ROOT/'experiments/balance-v27/cave-diamonds-v27-upper25-test.mcpack'
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            files={p.relative_to(V27).as_posix():p.read_bytes() for p in V27.rglob('*') if p.is_file()}
            self.assertEqual(set(z.namelist()),set(files))
            for name,content in files.items():
                self.assertEqual(z.read(name),content)
