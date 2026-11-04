import unittest
from tools.vanilla_reference import analyze


class VanillaReferenceTest(unittest.TestCase):
    def test_exposure_depth_and_connected_deposits(self):
        def ore(x,y,z,neighbors,kind='minecraft:deepslate_diamond_ore'):
            return {'x':x,'y':y,'z':z,'type':kind,'neighbours':neighbors}
        rock=['minecraft:deepslate']*6
        scan={'ores': [ore(2,-57,2,['minecraft:air','minecraft:water']+rock[:4]),
                       ore(3,-57,2,rock),
                       ore(8,-2,8,['minecraft:water']+rock[:5]),
                       ore(10,1,10,['minecraft:lava']+rock[:5],'minecraft:diamond_ore')]}
        result=analyze(scan,0,0,16)
        self.assertEqual(result['blocks'], {'total':4,'air':1,'fluid_only':2,'buried':1,'air_and_fluid':1,'water_adjacent':2,'lava_adjacent':1})
        self.assertEqual(result['below_zero']['total'],3)
        self.assertEqual(result['y_minus57']['total'],2)
        self.assertEqual(result['tunnel_band']['total'],2)
        self.assertEqual(result['deepslate_ore']['total'],3)
        self.assertEqual(result['deposits']['total'],3)
        self.assertEqual(result['deposits']['air_adjacent'],1)
        self.assertEqual(result['deposits']['air_adjacent_sizes'],[2])
        self.assertEqual(result['deposits']['touching_scan_boundary'],0)
        self.assertEqual(result['deposits']['air_adjacent_touching_boundary'],0)

    def test_reject_duplicate_and_mark_truncated_vein(self):
        ore={'x':-16,'y':-64,'z':-16,'type':'minecraft:deepslate_diamond_ore','neighbours':['minecraft:stone']*6}
        self.assertEqual(analyze({'ores':[ore]},-16,-16,16)['deposits']['touching_scan_boundary'],1)
        with self.assertRaises(ValueError): analyze({'ores':[ore,ore]},-16,-16,16)

    def test_aggregation_rejects_overlapping_areas_for_same_seed(self):
        from tools.vanilla_reference import aggregate
        ore={'x':0,'y':-57,'z':0,'type':'minecraft:deepslate_diamond_ore','neighbours':['minecraft:stone']*6}
        summary=analyze({'ores':[ore]},0,0,16)
        a={'seed':42,'chunk_x':0,'chunk_z':0,'chunks_per_side':2,**summary}
        b={'seed':42,'chunk_x':1,'chunk_z':1,'chunks_per_side':2,**summary}
        with self.assertRaises(ValueError): aggregate([a,b])
        b['seed']=43
        result=aggregate([a,b])
        self.assertEqual(result['totals']['blocks']['total'],2)
        self.assertEqual(result['total_chunks'],8)
