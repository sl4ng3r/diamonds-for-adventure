import unittest
from tools.summarize_research import summarize


class ResearchSummaryTests(unittest.TestCase):
    def test_groups_exposure_and_chunk_edges_with_negative_coordinates(self):
        scan = {'ores': [
            {'x': -16, 'y': -57, 'z': -15, 'exposed': True, 'biome': 'caves'},
            {'x': -15, 'y': -57, 'z': -15, 'exposed': False, 'biome': 'caves'},
            {'x': -1, 'y': -57, 'z': -1, 'exposed': True, 'biome': 'plains'},
        ], 'biomes': {'-57': {'caves': 3}}}
        result = summarize(scan)
        self.assertEqual(result['edge'], {'total': 2, 'exposed': 2, 'buried': 0})
        self.assertEqual(result['interior'], {'total': 1, 'exposed': 0, 'buried': 1})
        self.assertEqual(result['ore_biomes']['caves']['total'], 2)
        self.assertEqual(result['sampled_biomes']['-57']['caves'], 3)

    def test_rejects_duplicate_positions(self):
        ore = {'x': 1, 'y': 2, 'z': 3, 'exposed': False}
        with self.assertRaises(ValueError):
            summarize({'ores': [ore, ore]})

    def test_restart_compare_checks_identity_and_exposure(self):
        from tools.compare_worlds import compare_restart
        a = {'ores': [{'x': -1, 'y': -57, 'z': 1, 'type': 'deepslate', 'exposed': True}]}
        b = {'ores': [{'x': -1, 'y': -57, 'z': 1, 'type': 'deepslate', 'exposed': False}]}
        self.assertEqual(compare_restart(a, a), {'removed': 0, 'added': 0, 'changed': 0})
        self.assertEqual(compare_restart(a, b), {'removed': 0, 'added': 0, 'changed': 1})

    def test_counts_report_real_net_type_changes_by_chunk(self):
        from tools.summarize_research import compare_block_counts
        before={'blockCounts': {'0,0': {'air': 5, 'water': 2}}}
        after={'blockCounts': {'0,0': {'air': 4, 'water': 3}}}
        self.assertEqual(compare_block_counts(before,after), {'0,0': {'air': -1, 'water': 1}})
