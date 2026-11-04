import unittest
from tools.balance_profiles import height_profile, exposure_profile


class BalanceProfileTest(unittest.TestCase):
    def test_boundaries_and_buried_classification(self):
        rock=['minecraft:stone']*6
        def ore(y,neighbors): return {'y':y,'neighbours':neighbors}
        scan={'ores':[ore(-64,rock),ore(-48,rock),ore(-47,rock),ore(-32,rock),
                      ore(-31,rock),ore(-16,rock),ore(-15,rock),ore(-1,rock),
                      ore(0,rock),ore(16,['minecraft:air']+rock[:5])]}
        result=height_profile(scan)
        self.assertEqual([result[name]['total'] for name in result],[2,2,2,2,2])
        self.assertEqual(result['0..16']['buried'],1)

    def test_exposure_counts_wall_floor_and_ceiling_nonexclusively(self):
        rock=['minecraft:stone']*6
        def ore(y, faces):
            neighbours=rock.copy()
            for i in faces: neighbours[i]='minecraft:air'
            return {'y':y,'neighbours':neighbours}
        result=exposure_profile({'ores':[ore(-60,[0,2]),ore(-20,[3]),ore(0,[])]})
        self.assertEqual(result['air_exposed'],2)
        self.assertEqual(result['floor'],1)
        self.assertEqual(result['wall'],1)
        self.assertEqual(result['ceiling'],1)
        self.assertEqual(result['only_wall'],0)
        self.assertEqual(result['only_floor'],0)
        self.assertEqual(result['only_ceiling'],1)
        self.assertEqual(result['air_by_height']['-64..-48'],1)
        self.assertEqual(result['air_by_height']['-31..-16'],1)
