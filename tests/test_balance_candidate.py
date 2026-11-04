import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.balance_experiment import create_candidate, pack_digest, write_result_once, evaluate_mining, diff_ore_trace, probe_surfaces


class BalanceCandidateTest(unittest.TestCase):
    def test_candidate_is_isolated_and_uses_normal_ore(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        original=(source/'manifest.json').read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack')
            manifest=json.loads((pack/'manifest.json').read_text())
            self.assertEqual({m['type'] for m in manifest['modules']},{'data'})
            self.assertIn('Test',manifest['header']['name'])
            self.assertEqual(manifest['header']['min_engine_version'],[1,26,60])
            cave=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(cave['description']['places_feature'],'cavediamonds:cave_snap_floor')
            self.assertEqual(cave['distribution']['iterations'],1)
            buried=json.loads((pack/'feature_rules/sparse_buried_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(buried['distribution']['y']['extent'],[-64,-32])
            self.assertEqual(buried['distribution']['iterations'],1)
            ore=json.loads((pack/'features/sparse_buried.json').read_text())['minecraft:ore_feature']
            self.assertEqual({r['places_block'] for r in ore['replace_rules']},{'minecraft:diamond_ore','minecraft:deepslate_diamond_ore'})
            for file,expected in [('cave_diamond','minecraft:diamond_ore'),('cave_deepslate','minecraft:deepslate_diamond_ore')]:
                feature=json.loads((pack/'features'/f'{file}.json').read_text())['minecraft:single_block_feature']
                self.assertEqual(feature['places_block'],expected)
            self.assertFalse((pack/'feature_rules/thin_overworld.json').exists())
            self.assertFalse((pack/'features/scan_chunk.json').exists())
        self.assertEqual((source/'manifest.json').read_bytes(),original)

    def test_refuses_overwrite(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'pack'; target.mkdir(); (target/'keep').write_text('keep')
            with self.assertRaises(FileExistsError): create_candidate(source,target)
            self.assertEqual((target/'keep').read_text(),'keep')

    def test_pack_fingerprint_changes_with_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            pack=Path(directory); (pack/'a.json').write_text('one')
            first=pack_digest(pack)
            self.assertEqual(first,pack_digest(pack))
            (pack/'a.json').write_text('two')
            self.assertNotEqual(first,pack_digest(pack))

    def test_second_profile_keeps_generation_above_minus32(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v2')
            cave=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']
            buried=json.loads((pack/'feature_rules/sparse_buried_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(cave['distribution']['iterations'],2)
            self.assertEqual(buried['distribution']['iterations'],2)
            self.assertEqual(buried['distribution']['y']['extent'],[-64,16])

    def test_third_profile_varies_only_cave_attempts(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v3')
            cave=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']
            buried=json.loads((pack/'feature_rules/sparse_buried_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(cave['distribution']['iterations'],3)
            self.assertEqual(buried['distribution']['iterations'],2)
            self.assertEqual(buried['distribution']['y']['extent'],[-64,16])

    def test_fourth_profile_adds_one_cave_attempt(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v4')
            cave=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']
            buried=json.loads((pack/'feature_rules/sparse_buried_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(cave['distribution']['iterations'],4)
            self.assertEqual(buried['distribution']['iterations'],2)

    def test_fifth_profile_adds_at_most_one_adjacent_block_per_attempt(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v5')
            snap=json.loads((pack/'features/cave_snap_floor.json').read_text())['minecraft:snap_to_surface_feature']
            self.assertEqual(snap['feature_to_snap'],'cavediamonds:cave_pair')
            pair=json.loads((pack/'features/cave_pair.json').read_text())['minecraft:aggregate_feature']
            self.assertEqual(set(pair['features']),{'cavediamonds:cave_select','cavediamonds:cave_neighbor_chance'})
            chance=json.loads((pack/'features/cave_neighbor_chance.json').read_text())['minecraft:scatter_feature']
            self.assertEqual(chance['distribution']['iterations'],1)
            choices=json.loads((pack/'features/cave_neighbor_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choices),5)
            for ref,weight in choices:
                feature=json.loads((pack/'features'/f'{ref.split(":")[1]}.json').read_text())['minecraft:scatter_feature']
                distribution=feature['distribution']
                self.assertEqual(sum(abs(distribution[axis]) for axis in 'xyz'),1)
                self.assertEqual(distribution['iterations'],1)

    def test_sixth_profile_reduces_second_block_and_adds_optional_attempt(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v6')
            chance=json.loads((pack/'features/cave_neighbor_chance.json').read_text())['minecraft:scatter_feature']
            self.assertEqual(chance['distribution']['scatter_chance'],40)
            rule=json.loads((pack/'feature_rules/cave_extra_rule.json').read_text())['minecraft:feature_rules']
            self.assertEqual(rule['distribution']['iterations'],1)
            self.assertEqual(rule['distribution']['scatter_chance'],30)
            self.assertEqual(rule['description']['places_feature'],'cavediamonds:cave_snap_floor')

    def test_seventh_profile_weights_depth_and_chooses_three_surfaces(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v7')
            selector=json.loads((pack/'features/cave_snap_choice.json').read_text())['minecraft:weighted_random_feature']
            self.assertEqual({row[0] for row in selector['features']},
                             {'cavediamonds:cave_snap_floor','cavediamonds:cave_snap_ceiling','cavediamonds:cave_snap_wall'})
            for surface in ('floor','ceiling','wall'):
                snap=json.loads((pack/'features'/f'cave_snap_{surface}.json').read_text())['minecraft:snap_to_surface_feature']
                self.assertEqual(snap['surface'],surface)
                self.assertEqual(snap['feature_to_snap'],'cavediamonds:cave_pair')
                self.assertEqual(snap['search_range'],12)
            rules=[json.loads(p.read_text())['minecraft:feature_rules'] for p in (pack/'feature_rules').glob('cave_*rule.json')]
            self.assertEqual({tuple(r['distribution']['y']['extent']) for r in rules},{(-64,-33),(-32,-1),(0,4)})
            self.assertTrue(all(r['description']['places_feature']=='cavediamonds:cave_snap_choice' for r in rules))
            self.assertGreater(next(r['distribution']['iterations'] for r in rules if r['distribution']['y']['extent']==[-64,-33]),
                               next(r['distribution']['iterations'] for r in rules if r['distribution']['y']['extent']==[-32,-1]))

    def test_eighth_profile_weights_probability_per_height_downward(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v8')
            rules=[json.loads(p.read_text())['minecraft:feature_rules']['distribution'] for p in (pack/'feature_rules').glob('cave_*rule.json')]
            def density(extent):
                dist=next(d for d in rules if d['y']['extent']==extent)
                return dist['iterations'] * dist.get('scatter_chance',100)/100/(extent[1]-extent[0]+1)
            self.assertGreater(density([-64,-33]),density([-32,-1]))
            self.assertGreater(density([-32,-1]),density([0,4]))

    def test_atomic_result_write_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'area-00.json'
            write_result_once(target,{'value':1})
            with self.assertRaises(FileExistsError): write_result_once(target,{'value':2})
            self.assertEqual(json.loads(target.read_text()),{'value':1})

    def test_surface_probe_never_overwrites_existing_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            target=root/'surface-probes.json'
            target.write_text('keep')
            with patch('tools.balance_experiment.eula_accepted',return_value=True), patch('tools.balance_experiment.run') as run:
                with self.assertRaises(FileExistsError): probe_surfaces(root,root)
                run.assert_not_called()
            self.assertEqual(target.read_text(),'keep')

    def test_all_custom_feature_references_resolve(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        for profile in ('v3','v5','v6','v7','v8'):
          with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile=profile)
            ids=set(); references=[]
            for path in (pack/'features').glob('*.json'):
                doc=json.loads(path.read_text())
                body=next(v for k,v in doc.items() if k.startswith('minecraft:'))
                identifier=body['description']['identifier']
                self.assertNotIn(identifier,ids)
                ids.add(identifier)
                references.extend(item[0] if isinstance(item,list) else item for item in body.get('features',[]))
                references.extend(body[k] for k in ('places_feature','feature_to_snap') if k in body)
            for path in (pack/'feature_rules').glob('*.json'):
                rule=json.loads(path.read_text())['minecraft:feature_rules']
                references.append(rule['description']['places_feature'])
            self.assertTrue(references)
            self.assertTrue(all(reference in ids for reference in references))

    def test_simulated_mining_checks_modified_chunk_separately(self):
        def ore(x,z): return {'x':x,'y':-57,'z':z,'type':'minecraft:deepslate_diamond_ore'}
        mined=ore(-16,0)
        before={'ores':[mined,ore(-15,0),ore(0,0)]}
        after={'ores':[ore(-15,0),ore(1,0)]}
        result=evaluate_mining(before,after,mined)
        self.assertFalse(result['mined_ore_reappeared'])
        self.assertEqual(result['other_changes_modified_chunk'],0)
        self.assertEqual(result['changes_other_chunks'],2)

    def test_independent_reference_can_be_loaded_without_changing_default(self):
        from tools.balance_experiment import read_reference
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'holdout.json'
            path.write_text(json.dumps({'server_version':'1.26.61.1','areas':[]}))
            self.assertEqual(read_reference(path)['areas'],[])

    def test_trace_comparison_counts_exact_type_and_coordinates(self):
        before={'oreTrace':[[-1,-20,2,'minecraft:iron_ore'],[1,-20,2,'minecraft:deepslate_lapis_ore']]}
        after={'oreTrace':[[-1,-20,2,'minecraft:iron_ore'],[2,-20,2,'minecraft:deepslate_lapis_ore']]}
        diff=diff_ore_trace(before,after)
        self.assertEqual(diff['removed'],[[1,-20,2,'minecraft:deepslate_lapis_ore']])
        self.assertEqual(diff['added'],[[2,-20,2,'minecraft:deepslate_lapis_ore']])
