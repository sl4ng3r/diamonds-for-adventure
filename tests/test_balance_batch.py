import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.balance_batch import compact_status, exposure_summary, inspect_results, ratio, run_pending, surface_probe_summary
from tools.balance_experiment import pack_digest


class BatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pack = self.root / 'pack'
        self.pack.mkdir()
        (self.pack / 'manifest.json').write_text('{}')
        self.reference = self.root / 'reference.json'
        self.areas = [{'seed': i, 'chunk_x': i, 'chunk_z': -i, 'chunks_per_side': 4} for i in range(3)]
        self.reference.write_text(json.dumps({'server_version': '1.26.61.1', 'areas': self.areas}))
        self.results = self.root / 'results'
        self.results.mkdir()

    def save_area(self, index, **changes):
        value = {'index': index, **self.areas[index], 'pack_sha256': pack_digest(self.pack),
                 'reference_sha256': hashlib.sha256(self.reference.read_bytes()).hexdigest()}
        value.update(changes)
        (self.results / f'area-{index:02}.json').write_text(json.dumps(value))

    def test_resume_only_missing_and_limit(self):
        self.save_area(0)
        with patch('tools.balance_batch.scan_area') as scan:
            run_pending(self.pack, self.results, self.reference, limit=1)
        self.assertEqual(scan.call_count, 1)
        self.assertEqual(scan.call_args.args[2], 1)

    def test_rejects_mixed_pack_and_wrong_region(self):
        self.save_area(0, pack_sha256='wrong')
        with self.assertRaises(ValueError): inspect_results(self.pack, self.results, self.reference)
        self.save_area(0, seed=99)
        with self.assertRaises(ValueError): inspect_results(self.pack, self.results, self.reference)

    def test_rejects_invalid_result_filename_and_index(self):
        self.save_area(0)
        (self.results / 'area-00.json').rename(self.results / 'area-01.json')
        with self.assertRaises(ValueError): inspect_results(self.pack, self.results, self.reference)

    def test_ratios_handle_zero_baseline(self):
        self.assertIsNone(ratio(2, 0))
        self.assertEqual(ratio(15, 23), 65.2)

    def test_partial_report_does_not_claim_release(self):
        self.save_area(0)
        def total(groups, y, band):
            return {'deposits': {'air_adjacent': groups}, 'y_minus57': {'buried': y},
                    'tunnel_band': {'buried': band}}
        summary = {'vanilla': {'totals': total(23, 104, 367)},
                   'candidate': {'totals': total(15, 7, 32)},
                   'tunnel_contacts': {'vanilla': 640, 'candidate': 47}}
        with patch('tools.balance_batch.summarize', return_value=summary):
            status = compact_status(self.pack, self.results, self.reference)
        self.assertEqual(status['missing'], [1, 2])
        self.assertEqual(status['measurements']['air_adjacent_groups']['percent_of_vanilla'], 65.2)
        self.assertIn('No release decision', status['limitations'])

    def test_no_scan_when_results_have_wrong_reference_hash(self):
        self.save_area(0, reference_sha256='wrong')
        with patch('tools.balance_batch.scan_area') as scan:
            with self.assertRaises(ValueError):
                run_pending(self.pack, self.results, self.reference)
        scan.assert_not_called()

    def test_exposure_and_upper_scan_report_missing_instead_of_zero(self):
        self.save_area(0)
        self.assertIsNone(exposure_summary(self.results)['candidate_upper_17_to_40'])
        baseline=self.root/'baseline.json'
        candidate=self.root/'candidate'
        candidate.mkdir()
        scan={'ores':[{'y':-50,'neighbours':['minecraft:air']+['minecraft:stone']*5}]}
        baseline.write_text(json.dumps(scan))
        (candidate/'ore_scan.json').write_text(json.dumps(scan))
        self.save_area(0,reference_world_scan=str(baseline),candidate_world=str(candidate),candidate_upper_diamonds_17_to_40=2)
        result=exposure_summary(self.results)
        self.assertEqual(result['candidate']['wall'],1)
        self.assertEqual(result['candidate_upper_17_to_40'],2)

    def test_surface_probe_summary_detects_mismatched_pack(self):
        path=self.root/'probe.json'
        path.write_text(json.dumps({'pack_sha256':'other','probes':[{'surface':'wall','placed':True,'ore_on_face':1}]}))
        with self.assertRaises(ValueError): surface_probe_summary(path,pack_digest(self.pack))
        path.write_text(json.dumps({'pack_sha256':pack_digest(self.pack),'probes':[{'surface':'wall','placed':True,'ore_on_face':1},{'surface':'wall','placed':False,'ore_on_face':0}]}))
        self.assertEqual(surface_probe_summary(path,pack_digest(self.pack))['wall'],{'attempts':2,'on_face':1})

if __name__ == '__main__':
    unittest.main()
