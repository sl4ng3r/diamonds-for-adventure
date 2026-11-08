import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.balance_experiment import create_candidate, pack_digest, write_result_once, evaluate_mining, diff_ore_trace, probe_surfaces
from tools.holdout_uncertainty import percentile, report


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

    def test_ninth_profile_has_weighted_connected_attempts(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v9')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            weights={int(ref.rsplit('_',1)[1]):weight for ref,weight in choice}
            self.assertEqual(weights,{1:5,2:15,3:35,4:35,5:10})
            for n in weights:
                refs=json.loads((pack/'features'/f'cave_vein_{n}.json').read_text())['minecraft:aggregate_feature']['features']
                self.assertEqual(len(refs),n)
            snap=json.loads((pack/'features/cave_snap_wall.json').read_text())['minecraft:snap_to_surface_feature']
            self.assertEqual(snap['feature_to_snap'],'cavediamonds:cave_vein_choice')

    def test_tenth_profile_randomizes_direction_orders_and_biases_depth(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v10')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),25)
            size_weights={1:5,2:15,3:35,4:35,5:10}
            observed={}
            orders=set()
            for ref,weight in choice:
                name=ref.rsplit(':',1)[1]
                rotation,size=(int(part[1:]) for part in name.split('_')[2:])
                observed[size]=observed.get(size,[])+[weight]
                refs=json.loads((pack/'features'/f'{name}.json').read_text())['minecraft:aggregate_feature']['features']
                self.assertEqual(len(refs),size)
                orders.add(tuple(refs[1:]))
            self.assertEqual({size:weights for size,weights in observed.items()},
                             {size:[weight]*5 for size,weight in size_weights.items()})
            self.assertGreaterEqual(len(orders),5)
            rules=[json.loads(p.read_text())['minecraft:feature_rules'] for p in (pack/'feature_rules').glob('cave_*rule.json')]
            extents={tuple(r['distribution']['y']['extent']) for r in rules}
            self.assertEqual(extents,{(-64,-48),(-47,-1),(0,4)})
            def density(extent):
                dist=next(r['distribution'] for r in rules if r['distribution']['y']['extent']==list(extent))
                return dist['iterations'] * dist.get('scatter_chance',100)/100/(extent[1]-extent[0]+1)
            self.assertGreater(density((-64,-48)),density((-47,-1)))
            self.assertGreater(density((-47,-1)),density((0,4)))
            high=next(r['distribution'] for r in rules if r['distribution']['y']['extent']==[0,4])
            self.assertEqual(high['scatter_chance'],5)

    def test_eleventh_profile_keeps_randomized_veins_horizontal(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v11')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),40)
            orders=set()
            for ref,_weight in choice:
                name=ref.rsplit(':',1)[1]
                refs=json.loads((pack/'features'/f'{name}.json').read_text())['minecraft:aggregate_feature']['features'][1:]
                orders.add(tuple(refs))
                self.assertNotIn('cavediamonds:cave_neighbor_down',refs)
            self.assertGreaterEqual(len(orders),8)

    def test_twelfth_profile_adds_only_a_deep_probability_pass(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v12')
            extra=json.loads((pack/'feature_rules/cave_deep_extra.json').read_text())['minecraft:feature_rules']
            self.assertEqual(extra['distribution']['y']['extent'],[-64,-48])
            self.assertEqual(extra['distribution']['scatter_chance'],80)
            self.assertEqual(extra['description']['places_feature'],'cavediamonds:cave_snap_choice')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),40)

    def test_thirteenth_profile_uses_one_broad_deep_pass(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v13')
            rules=[json.loads(p.read_text())['minecraft:feature_rules'] for p in (pack/'feature_rules').glob('cave_*rule.json')]
            self.assertEqual({tuple(r['distribution']['y']['extent']) for r in rules},{(-64,-33),(-32,-1),(0,4)})
            deep=next(r for r in rules if r['distribution']['y']['extent']==[-64,-33])
            self.assertEqual(deep['distribution']['iterations'],1)
            high=next(r for r in rules if r['distribution']['y']['extent']==[0,4])
            self.assertEqual(high['distribution']['scatter_chance'],5)

    def test_fourteenth_profile_thins_only_the_middle_cave_band(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v14')
            mid=json.loads((pack/'feature_rules/cave_mid_rule.json').read_text())['minecraft:feature_rules']['distribution']
            deep=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(mid['scatter_chance'],80)
            self.assertNotIn('scatter_chance',deep)

    def test_fifteenth_profile_uses_ninety_percent_middle_band(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v15')
            mid=json.loads((pack/'feature_rules/cave_mid_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(mid['scatter_chance'],90)

    def test_sixteenth_profile_doubles_deep_pass_and_disables_upper_band(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v16')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),40)
            orders=set()
            for ref,_weight in choice:
                name=ref.rsplit(':',1)[1]
                refs=json.loads((pack/'features'/f'{name}.json').read_text())['minecraft:aggregate_feature']['features'][1:]
                orders.add(tuple(refs))
                self.assertNotIn('cavediamonds:cave_neighbor_down',refs)
            self.assertGreaterEqual(len(orders),8)
            deep=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']['distribution']
            mid=json.loads((pack/'feature_rules/cave_mid_rule.json').read_text())['minecraft:feature_rules']['distribution']
            high=json.loads((pack/'feature_rules/cave_high_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(deep['iterations'],2)
            self.assertEqual(deep['y']['extent'],[-64,-33])
            self.assertEqual(mid['y']['extent'],[-32,-1])
            self.assertEqual(high['scatter_chance'],0)

    def test_seventeenth_profile_keeps_one_deep_pass_and_disables_upper_band(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v17')
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),40)
            orders=set()
            for ref,_weight in choice:
                name=ref.rsplit(':',1)[1]
                refs=json.loads((pack/'features'/f'{name}.json').read_text())['minecraft:aggregate_feature']['features'][1:]
                orders.add(tuple(refs))
                self.assertNotIn('cavediamonds:cave_neighbor_down',refs)
            self.assertGreaterEqual(len(orders),8)
            deep=json.loads((pack/'feature_rules/cave_rule.json').read_text())['minecraft:feature_rules']['distribution']
            mid=json.loads((pack/'feature_rules/cave_mid_rule.json').read_text())['minecraft:feature_rules']['distribution']
            high=json.loads((pack/'feature_rules/cave_high_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(deep['iterations'],1)
            self.assertEqual(mid['scatter_chance'],90)
            self.assertEqual(high['scatter_chance'],0)

    def test_eighteenth_profile_omits_upper_feature_rule(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v18')
            self.assertTrue((pack/'feature_rules/cave_rule.json').exists())
            self.assertTrue((pack/'feature_rules/cave_mid_rule.json').exists())
            self.assertFalse((pack/'feature_rules/cave_high_rule.json').exists())
            choice=json.loads((pack/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            self.assertEqual(len(choice),40)

    def test_nineteenth_profile_adds_half_probability_deep_pass_and_third_buried_pass(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            pack=create_candidate(source,Path(directory)/'pack',profile='v19')
            extra=json.loads((pack/'feature_rules/cave_deep_extra.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(extra['y']['extent'],[-64,-33])
            self.assertEqual(extra['scatter_chance'],50)
            self.assertFalse((pack/'feature_rules/cave_high_rule.json').exists())
            buried=json.loads((pack/'feature_rules/sparse_buried_rule.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(buried['iterations'],3)

    def test_twentieth_profile_changes_only_deep_chance(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v19',profile='v19')
            candidate=create_candidate(source,Path(directory)/'v20',profile='v20')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json':
                    a['header']['name']=b['header']['name']
                if str(relative)=='feature_rules/cave_deep_extra.json':
                    self.assertEqual(b['minecraft:feature_rules']['distribution']['scatter_chance'],70)
                    a['minecraft:feature_rules']['distribution']['scatter_chance']=70
                self.assertEqual(a,b,str(relative))

    def test_twenty_first_profile_adds_only_one_probabilistic_deep_rule(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v19',profile='v19')
            candidate=create_candidate(source,Path(directory)/'v21',profile='v21')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json': a['header']['name']=b['header']['name']
                self.assertEqual(a,b,str(relative))
            extra=json.loads((candidate/'feature_rules/cave_deep_extra2.json').read_text())['minecraft:feature_rules']
            self.assertEqual(extra['distribution']['scatter_chance'],0.3)
            self.assertEqual(extra['description']['identifier'],'cavediamonds:cave_deep_extra2')

    def test_twenty_second_profile_adds_distinct_deep_band(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v19',profile='v19')
            candidate=create_candidate(source,Path(directory)/'v22',profile='v22')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json': a['header']['name']=b['header']['name']
                self.assertEqual(a,b,str(relative))
            dist=json.loads((candidate/'feature_rules/cave_deep_extra2.json').read_text())['minecraft:feature_rules']['distribution']
            self.assertEqual(dist['y']['extent'],[-52,-41])
            self.assertNotIn('scatter_chance',dist)

    def test_twenty_third_profile_thins_only_v22_extra_rule(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v22',profile='v22')
            candidate=create_candidate(source,Path(directory)/'v23',profile='v23')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json': a['header']['name']=b['header']['name']
                if str(relative)=='feature_rules/cave_deep_extra2.json':
                    self.assertEqual(b['minecraft:feature_rules']['distribution']['scatter_chance'],0.4)
                    a['minecraft:feature_rules']['distribution']['scatter_chance']=0.4
                self.assertEqual(a,b,str(relative))

    def test_twenty_fourth_profile_changes_only_v23_chance(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v23',profile='v23')
            candidate=create_candidate(source,Path(directory)/'v24',profile='v24')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json': a['header']['name']=b['header']['name']
                if str(relative)=='feature_rules/cave_deep_extra2.json':
                    self.assertEqual(b['minecraft:feature_rules']['distribution']['scatter_chance'],40)
                    a['minecraft:feature_rules']['distribution']['scatter_chance']=40
                self.assertEqual(a,b,str(relative))

    def test_twenty_fifth_profile_changes_only_vein_weights(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v24',profile='v24')
            candidate=create_candidate(source,Path(directory)/'v25',profile='v25')
            for path in base.rglob('*.json'):
                relative=path.relative_to(base)
                a=json.loads(path.read_text()); b=json.loads((candidate/relative).read_text())
                if str(relative)=='manifest.json':
                    a['header']['name']=b['header']['name']
                    a['header']['description']=b['header']['description']
                if str(relative)=='features/cave_vein_choice.json':
                    for entry in a['minecraft:weighted_random_feature']['features']:
                        size=int(entry[0].rsplit('_n',1)[1])
                        entry[1]={'1':1,'2':2,'3':35,'4':52,'5':10}[str(size)]
                self.assertEqual(a,b,str(relative))
            choice=json.loads((candidate/'features/cave_vein_choice.json').read_text())['minecraft:weighted_random_feature']['features']
            weights={}
            for ref,weight in choice:
                size=int(ref.rsplit('_n',1)[1]); weights.setdefault(size,set()).add(weight)
            self.assertEqual(weights,{1:{1},2:{2},3:{35},4:{52},5:{10}})
            self.assertEqual(json.loads((candidate/'manifest.json').read_text())['header']['name'],'Cave Diamonds – Balance Test v25 (nicht freigegeben)')

    def test_twenty_sixth_profile_further_favors_four_block_veins(self):
        source=Path(__file__).resolve().parents[1]/'prototype/behavior_pack'
        with tempfile.TemporaryDirectory() as directory:
            base=create_candidate(source,Path(directory)/'v25',profile='v25')
            candidate=create_candidate(source,Path(directory)/'v26',profile='v26')
            base_choice=json.loads((base/'features/cave_vein_choice.json').read_text())
            candidate_choice=json.loads((candidate/'features/cave_vein_choice.json').read_text())
            base_weights={int(row[0].rsplit('_n',1)[1]):row[1] for row in base_choice['minecraft:weighted_random_feature']['features']}
            candidate_weights={int(row[0].rsplit('_n',1)[1]):row[1] for row in candidate_choice['minecraft:weighted_random_feature']['features']}
            self.assertEqual(base_weights,{1:1,2:2,3:35,4:52,5:10})
            self.assertEqual(candidate_weights,{1:1,2:1,3:25,4:64,5:10})
            self.assertEqual(json.loads((candidate/'manifest.json').read_text())['header']['name'],'Cave Diamonds – Balance Test v26 (nicht freigegeben)')

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
        for profile in ('v3','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19','v25','v26'):
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

    def test_holdout_uncertainty_resamples_complete_areas(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            template={
                'vanilla':{'deposits':{'air_adjacent':10},'y_minus57':{'buried':20}},
                'candidate':{'deposits':{'air_adjacent':5},'y_minus57':{'buried':4}},
                'tunnel_contacts':{'vanilla':30,'candidate':3},
            }
            for index,seed in enumerate((1,2)):
                data=dict(template)
                data['seed']=seed
                data['vanilla']=dict(template['vanilla'])
                data['candidate']=dict(template['candidate'])
                data['vanilla']['deposits']=dict(template['vanilla']['deposits'])
                data['candidate']['deposits']=dict(template['candidate']['deposits'])
                root.joinpath(f'area-{index:02d}.json').write_text(json.dumps(data))
            result=report(root,bootstrap_samples=100)
            self.assertEqual(result['areas'],2)
            self.assertEqual(result['metrics']['air_groups']['percent_of_vanilla'],50.0)
            self.assertEqual(result['metrics']['y_minus57']['percent_of_vanilla'],20.0)
            self.assertAlmostEqual(percentile([1,3],0.5),2.0)
