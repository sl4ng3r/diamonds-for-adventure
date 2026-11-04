import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'prototype/behavior_pack'

class ContractTests(unittest.TestCase):
    def load(self, path):
        return json.loads((PACK / path).read_text())

    def test_manifest_is_behavior_pack_without_scripts(self):
        manifest = self.load('manifest.json')
        self.assertEqual([m['type'] for m in manifest['modules']], ['data'])
        self.assertNotEqual(manifest['header']['uuid'], manifest['modules'][0]['uuid'])

    def test_ore_replacement_and_exposure_contract(self):
        for ore, host, filename in [('minecraft:diamond_ore', 'minecraft:stone', 'thin_diamond.json'), ('minecraft:deepslate_diamond_ore', 'minecraft:deepslate', 'thin_deepslate.json')]:
            with self.subTest(ore=ore):
                obj = self.load('features/' + filename)['minecraft:single_block_feature']
                self.assertEqual(obj['may_replace'], [ore])
                self.assertEqual({x['block']: x['weight'] for x in obj['places_block']}, {host: 9, ore: 1})
                for direction in ('top', 'bottom', 'north', 'south', 'east', 'west'):
                    self.assertEqual(set(obj['may_not_attach_to'][direction]), {'minecraft:air', 'minecraft:water', 'minecraft:flowing_water', 'minecraft:lava', 'minecraft:flowing_lava'})

    def test_rule_and_grid_are_explicit(self):
        rule = self.load('feature_rules/thin_overworld.json')['minecraft:feature_rules']
        self.assertEqual(rule['conditions']['placement_pass'], 'final_pass')
        feature = self.load('features/scan_chunk.json')['minecraft:scatter_feature']['distribution']
        self.assertEqual(feature['iterations'], 20736)
        self.assertNotIn('scatter_chance', feature)
        self.assertEqual(feature['x']['extent'], [0,15])
        self.assertEqual(feature['z']['extent'], [0,15])
        self.assertEqual(feature['y']['extent'], [0,80])
        self.assertTrue(all(feature[a]['distribution'] == 'fixed_grid' and feature[a]['step_size'] == 1 for a in 'xyz'))

    def test_references_resolve(self):
        ids = {}
        refs = []
        for path in (PACK / 'features').glob('*.json'):
            doc = json.loads(path.read_text())
            body = next(v for k,v in doc.items() if k.startswith('minecraft:'))
            ids[body['description']['identifier']] = path
            if 'places_feature' in body: refs.append(body['places_feature'])
            refs += body.get('features', [])
        rule = self.load('feature_rules/thin_overworld.json')['minecraft:feature_rules']
        refs.append(rule['description']['places_feature'])
        for ref in refs: self.assertIn(ref, ids)
        self.assertEqual(len(ids), len(list((PACK / 'features').glob('*.json'))))

if __name__ == '__main__': unittest.main()
