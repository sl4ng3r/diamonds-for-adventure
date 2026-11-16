import json
import tempfile
import unittest
from pathlib import Path

from tools.balance_followup import summarize_rows, load_plan, exposure_interval


class BalanceFollowupTest(unittest.TestCase):
    def test_plan_freezes_pack_reference_and_all_regions(self):
        import hashlib
        from tools.balance_experiment import pack_digest
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            pack=root/'pack';pack.mkdir();(pack/'manifest.json').write_text('{}')
            ref=root/'ref.json'
            areas=[{'seed':42,'chunk_x':1,'chunk_z':-2,'chunks_per_side':4,'scan_file':'scan.json'}]
            ref.write_text(json.dumps({'server_version':'1.26.61.1','areas':areas}))
            plan={'server_version':'1.26.61.1','pack':'pack','pack_sha256':pack_digest(pack),
                  'reference':'ref.json','reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),
                  'results':'results','indexes':[0],
                  'areas':[{k:areas[0][k] for k in ('seed','chunk_x','chunk_z','chunks_per_side')}]}
            path=root/'plan.json';path.write_text(json.dumps(plan))
            self.assertEqual(load_plan(path,root),(pack.resolve(),(root/'results').resolve(),ref.resolve()))
            (pack/'manifest.json').write_text('{"changed":true}')
            with self.assertRaises(ValueError): load_plan(path,root)

    def test_compact_summary_counts_full_groups_and_upper_heights(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            rows=[]
            for index,(vanilla,candidate,heights) in enumerate(((10,12,[24,24]),(20,22,[18]))):
                world=root/'data/research'/f'area-{index}'
                world.mkdir(parents=True)
                (world/'ore_scan.json').write_text(json.dumps({
                    'ores':[{'y':-40,'neighbours':['minecraft:air']},
                            {'y':-30,'neighbours':['minecraft:stone']}],
                    'upperDiamondOre':[{'y':y,'neighbours':['minecraft:air']} for y in heights]}))
                baseline=root/'data/research'/f'vanilla-{index}.json'
                baseline.write_text(json.dumps({'ores':[{'y':-40,'neighbours':['minecraft:air']}],
                                                'upperDiamondOre':[]}))
                rows.append({'index':index,'candidate_world':str(world.relative_to(root)),
                             'reference_world_scan':str(baseline.relative_to(root)),
                             'candidate_upper_diamonds_17_to_40':len(heights),
                             'full_height':{'range':[-64,40],
                                            'vanilla_source':'reference_assuming_no_upper_diamonds',
                                            'vanilla_air_groups':vanilla,
                                            'candidate':{'deposits':{'air_adjacent':candidate}}}})
            report=summarize_rows(rows,root)
            self.assertEqual(report['groups'],{'vanilla':30,'candidate':34,'percent_of_vanilla':113.3})
            self.assertEqual(report['upper_heights'],{'18':1,'24':2})
            self.assertEqual(report['highest_upper_y'],24)
            self.assertEqual([a['percent_of_vanilla'] for a in report['areas']],[120.0,110.0])
            self.assertEqual(report['air_exposed_blocks'],
                             {'vanilla':2,'candidate':5,'percent_of_vanilla':250.0})
            self.assertEqual(report['air_exposed_by_height']['-47..-32'],
                             {'vanilla':2,'candidate':2,'percent_of_vanilla':100.0})
            self.assertEqual(report['air_exposed_by_height']['17..40'],
                             {'vanilla':0,'candidate':3,'percent_of_vanilla':None})
            self.assertEqual([a['air_exposed_blocks'] for a in report['areas']],
                             [{'vanilla':1,'candidate':3,'percent_of_vanilla':300.0},
                              {'vanilla':1,'candidate':2,'percent_of_vanilla':200.0}])
            self.assertEqual(exposure_interval(report['areas'],1000),[200.0,300.0])

    def test_rejects_mismatched_upper_count_or_baseline_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            world=root/'data/research/area'
            world.mkdir(parents=True)
            (world/'ore_scan.json').write_text(json.dumps({'upperDiamondOre':[]}))
            row={'index':0,'candidate_world':str(world.relative_to(root)),
                 'candidate_upper_diamonds_17_to_40':1,
                 'full_height':{'range':[-64,40],
                                'vanilla_source':'reference_assuming_no_upper_diamonds',
                                'vanilla_air_groups':1,
                                'candidate':{'deposits':{'air_adjacent':1}}}}
            with self.assertRaises(ValueError): summarize_rows([row],root)
            row['candidate_upper_diamonds_17_to_40']=0
            row['full_height']['vanilla_source']='fresh_full_height_scan'
            with self.assertRaises(ValueError): summarize_rows([row],root)

    def test_exposure_interval_handles_zero_baseline(self):
        areas=[{'air_exposed_blocks':{'vanilla':0,'candidate':2}}]
        self.assertEqual(exposure_interval(areas,100),[None,None])
