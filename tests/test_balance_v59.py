import json
from pathlib import Path
import tempfile
import unittest

from tools.build_v59 import SOURCE, build_pack


class OceanCavesTest(unittest.TestCase):
    def test_adds_a_separate_ocean_rule_and_preserves_v57_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'pack')
            original = {path.relative_to(SOURCE): path.read_bytes()
                        for path in SOURCE.rglob('*.json') if path.name != 'manifest.json'}
            self.assertEqual(original, {path: (pack / path).read_bytes() for path in original})
            rule = json.loads((pack / 'feature_rules/ocean_cave_rule.json').read_text())
            rule = rule['minecraft:feature_rules']
            self.assertEqual(rule['conditions']['minecraft:biome_filter'],
                             {'test': 'has_biome_tag', 'value': 'ocean'})
            chance = json.loads((pack / 'features/ocean_cave_chance.json').read_text())
            self.assertLess(chance['minecraft:scatter_feature']['distribution']['scatter_chance'], 100)
            for surface in ('floor', 'ceiling', 'wall'):
                snap = json.loads((pack / f'features/ocean_cave_{surface}.json').read_text())
                snap = snap['minecraft:snap_to_surface_feature']
                self.assertEqual(snap['surface'], surface)
                self.assertEqual(snap['feature_to_snap'], 'cavediamonds:cave_select')
                self.assertTrue(snap['allow_underwater_placement'])
                self.assertTrue(snap['embed_in_surface'])
                self.assertFalse(snap['allow_air_placement'])
                self.assertFalse(snap['allow_non_air_placement'])
                # Bedrock includes the embedded position in the search range.
                self.assertEqual(rule['distribution']['y']['extent'][1] + snap['search_range'], 35)
