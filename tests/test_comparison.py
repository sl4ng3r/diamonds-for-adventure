import unittest
from tools.compare_worlds import parse_filled

class EulaConsentTest(unittest.TestCase):
    def test_requires_explicit_true_in_env_file(self):
        import tempfile
        from pathlib import Path
        from tools.compare_worlds import eula_accepted
        with tempfile.TemporaryDirectory() as directory:
            env = Path(directory) / '.env'
            self.assertFalse(eula_accepted(env))
            env.write_text('# EULA=TRUE\nEULA=FALSE\n')
            self.assertFalse(eula_accepted(env))
            env.write_text('EULA=TRUE\n')
            self.assertTrue(eula_accepted(env))

class ParseTest(unittest.TestCase):
    def test_normal_and_zero(self):
        self.assertEqual(parse_filled('[INFO] 127 blocks filled'), 127)
        self.assertEqual(parse_filled('[ERROR] 0 blocks filled'), 0)
        self.assertEqual(parse_filled('[INFO] 1 block filled'), 1)
        self.assertIsNone(parse_filled('[INFO] Server started.'))

class ScanParseTest(unittest.TestCase):
    def test_scan_marker(self):
        from tools.compare_worlds import parse_scan
        self.assertEqual(parse_scan('[Scripting] CAVEDIAMONDS_SCAN {"ores":[]}'), {'ores': []})
        self.assertIsNone(parse_scan('[INFO] no result'))

class CompareScanTest(unittest.TestCase):
    def test_compares_exact_positions_and_exposure(self):
        from tools.compare_worlds import compare_scans
        baseline = {'ores':[{'x':1,'y':-30,'z':2,'exposed':True}, {'x':2,'y':-30,'z':2,'exposed':False}, {'x':3,'y':-30,'z':2,'exposed':False}]}
        treated = {'ores':[{'x':1,'y':-30,'z':2,'exposed':True}, {'x':3,'y':-30,'z':2,'exposed':False}]}
        result = compare_scans(baseline, treated)
        self.assertEqual(result['baseline_buried'],2)
        self.assertEqual(result['buried_removed'],1)
        self.assertEqual(result['exposed_preserved'],1)
        self.assertEqual(result['new_coordinates'],0)

    def test_activation_inserts_pack_once_without_removing_other_packs(self):
        from tools.compare_worlds import enable_research_pack, PACK_ID
        old=[{'pack_id':'diagnostic','version':[0,1,0]}]
        result=enable_research_pack(old)
        self.assertEqual(result[0]['pack_id'],PACK_ID)
        self.assertEqual(result[1:],old)
        self.assertEqual(enable_research_pack(result),result)

class VirtualTunnelTest(unittest.TestCase):
    def test_wall_floor_and_roof_discovery(self):
        from tools.compare_worlds import count_tunnel_finds
        ores=[{'x':5,'y':-57,'z':3}, {'x':5,'y':-58,'z':3}, {'x':5,'y':-54,'z':3}]
        self.assertEqual(count_tunnel_finds(ores, 8, -57), {1:0,2:1,3:2,4:1,5:0,6:0})


class FullRemovalVariantTest(unittest.TestCase):
    def test_variant_does_not_change_prototype(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_full_removal_variant
        source = Path(__file__).resolve().parents[1] / 'prototype/behavior_pack'
        before = (source / 'features/thin_diamond.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            variant = create_full_removal_variant(source, Path(directory) / 'pack')
            for name, block in [('thin_diamond', 'minecraft:stone'), ('thin_deepslate', 'minecraft:deepslate')]:
                obj = json.loads((variant / 'features' / (name+'.json')).read_text())['minecraft:single_block_feature']
                self.assertEqual(obj['places_block'], block)
        self.assertEqual((source / 'features/thin_diamond.json').read_bytes(), before)

class ExposureIsolationVariantTest(unittest.TestCase):
    def test_optional_exposure_filter_removal_is_isolated(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_full_removal_variant
        source = Path(__file__).resolve().parents[1] / 'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant = create_full_removal_variant(source, Path(directory) / 'pack', ignore_exposure=True)
            for name in ('thin_diamond', 'thin_deepslate'):
                obj = json.loads((variant/'features'/(name+'.json')).read_text())['minecraft:single_block_feature']
                self.assertNotIn('may_not_attach_to', obj)
        obj = json.loads((source/'features/thin_diamond.json').read_text())['minecraft:single_block_feature']
        self.assertIn('may_not_attach_to', obj)

class OriginMarkerVariantTest(unittest.TestCase):
    def test_marker_is_a_separate_research_variant(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_full_removal_variant
        source = Path(__file__).resolve().parents[1] / 'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant = create_full_removal_variant(source, Path(directory) / 'pack', mark_origins=True)
            rule = json.loads((variant/'feature_rules/thin_overworld.json').read_text())['minecraft:feature_rules']
            self.assertEqual(rule['description']['places_feature'], 'cavediamonds:scan_with_marker')
            self.assertTrue((variant/'features/origin_marker.json').is_file())
        self.assertFalse((source/'features/origin_marker.json').exists())

class GridMarkerVariantTest(unittest.TestCase):
    def test_grid_marker_replaces_air_only_in_test_copy(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_full_removal_variant
        source = Path(__file__).resolve().parents[1] / 'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant = create_full_removal_variant(source, Path(directory) / 'pack', mark_grid=True)
            marker = json.loads((variant/'features/origin_marker.json').read_text())['minecraft:single_block_feature']
            self.assertEqual(marker['may_replace'], ['minecraft:air'])
            scan = json.loads((variant/'features/scan_chunk.json').read_text())['minecraft:scatter_feature']
            self.assertEqual(scan['places_feature'], 'cavediamonds:origin_marker')
            rule = json.loads((variant/'feature_rules/thin_overworld.json').read_text())['minecraft:feature_rules']
            self.assertEqual(rule['distribution']['y'], 220)

class UndergroundGridVariantTest(unittest.TestCase):
    def test_underground_grid_marks_only_host_rock(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_full_removal_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_full_removal_variant(source,Path(directory)/'pack',mark_underground=True)
            marker=json.loads((variant/'features/origin_marker.json').read_text())['minecraft:single_block_feature']
            self.assertEqual(set(marker['may_replace']),{'minecraft:stone','minecraft:deepslate'})
            rule=json.loads((variant/'feature_rules/thin_overworld.json').read_text())['minecraft:feature_rules']
            self.assertEqual(rule['distribution']['y'],-64)

class VanillaOverrideVariantTest(unittest.TestCase):
    def test_overrides_are_only_in_disposable_copy(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_vanilla_override_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_vanilla_override_variant(source,Path(directory)/'pack')
            self.assertFalse((variant/'feature_rules/thin_overworld.json').exists())
            for name in ('diamond_ore_feature','diamond_ore_large_feature','diamond_ore_buried_feature'):
                body=json.loads((variant/'features'/(name+'.json')).read_text())['minecraft:ore_feature']
                self.assertEqual(body['description']['identifier'],'minecraft:'+name)
                self.assertNotIn('diamond_ore',json.dumps(body['replace_rules']))
        self.assertTrue((source/'feature_rules/thin_overworld.json').is_file())

class CaveGenerationVariantTest(unittest.TestCase):
    def test_cave_generation_variant_only_places_vanilla_ore(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_cave_generation_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_cave_generation_variant(source,Path(directory)/'pack')
            for name,host,ore in [('cave_diamond','minecraft:stone','minecraft:diamond_ore'),('cave_deepslate','minecraft:deepslate','minecraft:deepslate_diamond_ore')]:
                obj=json.loads((variant/'features'/(name+'.json')).read_text())['minecraft:single_block_feature']
                self.assertEqual(obj['may_replace'],[host])
                self.assertEqual(obj['places_block'],ore)
                self.assertEqual(obj['may_attach_to']['min_sides_must_attach'],1)
                self.assertIn('minecraft:air',obj['may_attach_to']['all'])
            rule=json.loads((variant/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(rule['conditions']['placement_pass'],'final_pass')
        self.assertFalse((source/'feature_rules/cave_rule.json').exists())

class BuriedGenerationVariantTest(unittest.TestCase):
    def test_buried_variant_uses_both_vanilla_ore_types(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_buried_generation_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_buried_generation_variant(source,Path(directory)/'pack')
            obj=json.loads((variant/'features/sparse_buried.json').read_text())['minecraft:ore_feature']
            self.assertEqual(obj['discard_chance_on_air_exposure'],1.0)
            self.assertEqual({x['places_block'] for x in obj['replace_rules']},{'minecraft:diamond_ore','minecraft:deepslate_diamond_ore'})
            self.assertTrue((variant/'feature_rules/sparse_buried_rule.json').is_file())
        self.assertFalse((source/'feature_rules/sparse_buried_rule.json').exists())

class DirectionalCaveVariantTest(unittest.TestCase):
    def test_directional_features_use_explicit_faces(self):
        import json,tempfile
        from pathlib import Path
        from tools.compare_worlds import create_cave_generation_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_cave_generation_variant(source,Path(directory)/'pack',directional=True)
            for face in ('north','south','east','west','top','bottom'):
                obj=json.loads((variant/'features'/('cave_diamond_'+face+'.json')).read_text())['minecraft:single_block_feature']
                self.assertIn('minecraft:air',obj['may_attach_to'][face])
            aggregate=json.loads((variant/'features/cave_select.json').read_text())['minecraft:aggregate_feature']
            self.assertEqual(len(aggregate['features']),12)

class SnapCaveVariantTest(unittest.TestCase):
    def test_snap_variants_embed_in_valid_surface(self):
        import json,tempfile
        from pathlib import Path
        from tools.compare_worlds import create_snap_cave_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_snap_cave_variant(source,Path(directory)/'pack')
            for face in ('floor','ceiling'):
                obj=json.loads((variant/'features'/('cave_snap_'+face+'.json')).read_text())['minecraft:snap_to_surface_feature']
                self.assertEqual(obj['surface'],face)
                self.assertTrue(obj['embed_in_surface'])
                self.assertEqual(set(obj['allowed_surface_blocks']),{'minecraft:stone','minecraft:deepslate'})
                self.assertFalse(obj['allow_non_air_placement'])

    def test_research_pass_can_be_changed_without_touching_source(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_snap_cave_variant, set_cave_pass
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_snap_cave_variant(source,Path(directory)/'pack')
            set_cave_pass(variant,'after_underground_pass')
            rule=json.loads((variant/'feature_rules/cave_rule.json').read_text())
            self.assertEqual(rule['minecraft:feature_rules']['conditions']['placement_pass'],'after_underground_pass')
        self.assertFalse((source/'feature_rules/cave_rule.json').exists())

    def test_selects_single_cave_surface_in_research_copy(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_snap_cave_variant, set_snap_selection
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_snap_cave_variant(source,Path(directory)/'pack')
            set_snap_selection(variant,'floor')
            rule=json.loads((variant/'feature_rules/cave_rule.json').read_text())
            self.assertEqual(rule['minecraft:feature_rules']['description']['places_feature'],'cavediamonds:cave_snap_floor')

    def test_fixed_grid_scans_cave_positions_without_random_distribution(self):
        import json, tempfile
        from pathlib import Path
        from tools.compare_worlds import create_snap_cave_variant, set_cave_fixed_grid
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_snap_cave_variant(source,Path(directory)/'pack')
            set_cave_fixed_grid(variant)
            distribution=json.loads((variant/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(distribution['iterations'],176)
            for axis in 'xyz': self.assertEqual(distribution[axis]['distribution'],'fixed_grid')

class CombinedVariantTest(unittest.TestCase):
    def test_combines_both_rules_only_in_research_copy(self):
        import tempfile
        from pathlib import Path
        from tools.compare_worlds import create_combined_generation_variant
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            variant=create_combined_generation_variant(source,Path(directory)/'pack')
            self.assertTrue((variant/'feature_rules/cave_rule.json').is_file())
            self.assertTrue((variant/'feature_rules/sparse_buried_rule.json').is_file())
            self.assertFalse((variant/'feature_rules/thin_overworld.json').exists())
        self.assertTrue((source/'feature_rules/thin_overworld.json').exists())

class NegativeTunnelOriginTest(unittest.TestCase):
    def test_tunnel_coordinates_can_be_negative(self):
        from tools.compare_worlds import count_tunnel_finds
        ores=[{'x':-30,'y':-57,'z':-20}]
        result=count_tunnel_finds(ores, 16, -57, origin_x=-32, origin_z=-32)
        self.assertEqual(result[-21],1)
        self.assertEqual(result[-20],1)
        self.assertEqual(result[-19],1)

class PreloadOrderTest(unittest.TestCase):
    def test_direction_reverses_chunk_columns(self):
        from tools.compare_worlds import preload_columns
        self.assertEqual(preload_columns(-3, 3, 'east'), [-3, -2, -1])
        self.assertEqual(preload_columns(-3, 3, 'west'), [-1, -2, -3])

    def test_chunk_markers_stay_in_the_requested_chunks(self):
        from tools.compare_worlds import marker_positions
        self.assertEqual(marker_positions(-1, 2, 2), [(-16,300,32),(-16,300,48),(0,300,32),(0,300,48)])

    def test_runner_accepts_stability_and_marker_options(self):
        import inspect
        from tools.compare_worlds import run
        params = inspect.signature(run).parameters
        self.assertIn('stability_delay', params)
        self.assertIn('mark_saved_chunks', params)

    def test_mining_probe_prefers_exposed_ore(self):
        from tools.compare_worlds import choose_mining_probe
        ores=[{'x':0,'y':-30,'z':0,'exposed':False},{'x':1,'y':-30,'z':0,'exposed':True}]
        self.assertEqual(choose_mining_probe(ores), ores[1])
        self.assertIsNone(choose_mining_probe([]))

class TickingAreaWindowTest(unittest.TestCase):
    def test_padded_windows_cover_scan_and_neighbours_under_bedrock_limit(self):
        from tools.compare_worlds import ticking_area_windows
        for chunks in (4,8,9,10,16):
            windows=ticking_area_windows(chunks)
            self.assertTrue(all((x1-x0)*(z1-z0) <= 100 for x0,x1,z0,z1 in windows))
            self.assertTrue(all(any(x0 <= x < x1 and z0 <= z < z1 for x0,x1,z0,z1 in windows)
                                for x in range(-1,chunks+1) for z in range(-1,chunks+1)))
        self.assertEqual(len(ticking_area_windows(4)),1)
        self.assertEqual(len(ticking_area_windows(8)),1)
        self.assertEqual(len(ticking_area_windows(9)),4)
        self.assertEqual(len(ticking_area_windows(10)),4)
        self.assertEqual(len(ticking_area_windows(16)),4)

    def test_invalid_window_sizes_are_rejected(self):
        from tools.compare_worlds import ticking_area_windows
        for value in (0,-1,1.5,'4'):
            with self.assertRaises(ValueError): ticking_area_windows(value)
