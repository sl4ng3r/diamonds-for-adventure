import unittest
from tools.build_holdout_reference import match_plan


class HoldoutPlanTests(unittest.TestCase):
    def test_matches_in_plan_order_and_rejects_duplicates_or_missing(self):
        plan={'chunks_per_side':4,'areas':[{'seed':3,'chunk_x':1,'chunk_z':2},{'seed':4,'chunk_x':5,'chunk_z':6}]}
        a={'seed':3,'chunk_x':1,'chunk_z':2,'chunks_per_side':4}
        b={'seed':4,'chunk_x':5,'chunk_z':6,'chunks_per_side':4}
        self.assertEqual(match_plan(plan,[('b',b),('a',a)]),['a','b'])
        with self.assertRaises(ValueError): match_plan(plan,[('a',a)])
        with self.assertRaises(ValueError): match_plan(plan,[('a',a),('a2',a),('b',b)])
