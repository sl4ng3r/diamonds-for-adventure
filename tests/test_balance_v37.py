import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v37 import build_pack


ROOT=Path(__file__).resolve().parents[1]
V36=ROOT/'experiments/balance-v36/behavior_pack'
V37=ROOT/'experiments/balance-v37/behavior_pack'
WEIGHTS=((1,1),(2,1),(3,25),(4,64),(5,10))


class BalanceV37Test(unittest.TestCase):
    def test_floor_and_ceiling_place_neighbours_inward(self):
        old={p.relative_to(V36):p.read_bytes() for p in V36.rglob('*') if p.is_file()}
        new={p.relative_to(V37):p.read_bytes() for p in V37.rglob('*') if p.is_file()}
        self.assertEqual(set(old)-set(new),set())
        self.assertEqual({name for name in old if old[name]!=new[name]},
                         {Path('manifest.json')} |
                         {Path(f'features/cave_snap_{surface}{suffix}.json')
                          for surface in ('floor','ceiling') for suffix in ('','_upper')})
        for surface,step in (('floor',-1),('ceiling',1)):
            choice=json.loads(new[Path(f'features/cave_{surface}_vein_choice.json')])['minecraft:weighted_random_feature']
            self.assertEqual(choice['features'],
                             [[f'cavediamonds:cave_{surface}_vein_n{n}',weight] for n,weight in WEIGHTS])
            for suffix in ('','_upper'):
                snap=json.loads(new[Path(f'features/cave_snap_{surface}{suffix}.json')])['minecraft:snap_to_surface_feature']
                self.assertEqual(snap['feature_to_snap'],f'cavediamonds:cave_{surface}_vein_choice')
            for depth in (1,2,3):
                feature=json.loads(new[Path(f'features/cave_{surface}_inward_{depth}.json')])['minecraft:scatter_feature']
                self.assertEqual(feature['distribution']['y'],step*depth)
                self.assertEqual((feature['distribution']['x'],feature['distribution']['z']),(0,0))
            for n,_ in WEIGHTS:
                feature=json.loads(new[Path(f'features/cave_{surface}_vein_n{n}.json')])['minecraft:aggregate_feature']
                expected=['cavediamonds:cave_select']
                if n>=2: expected.append(f'cavediamonds:cave_{surface}_inward_1')
                if n>=3: expected.append(f'cavediamonds:cave_{surface}_inward_2')
                if n>=4: expected.append(f'cavediamonds:cave_{surface}_side_choice')
                if n>=5: expected.append(f'cavediamonds:cave_{surface}_inward_3')
                self.assertEqual(feature['features'],expected)

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'existing';target.mkdir()
            with self.assertRaises(FileExistsError): build_pack(target)


if __name__=='__main__': unittest.main()
