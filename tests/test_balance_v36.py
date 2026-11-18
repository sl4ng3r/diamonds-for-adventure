import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v36 import build_pack


ROOT=Path(__file__).resolve().parents[1]
V35=ROOT/'experiments/balance-v35/behavior_pack'
V36=ROOT/'experiments/balance-v36/behavior_pack'


class BalanceV36Test(unittest.TestCase):
    def test_veins_include_surface_anchor_and_buried_blob(self):
        old={p.relative_to(V35):p.read_bytes() for p in V35.rglob('*') if p.is_file()}
        new={p.relative_to(V36):p.read_bytes() for p in V36.rglob('*') if p.is_file()}
        self.assertEqual(set(old)-set(new),set())
        self.assertEqual(set(new)-set(old),
                         {Path(f'features/cave_surface_vein_n{n}.json') for n in range(1,6)})
        self.assertEqual({name for name in old if old[name]!=new[name]},
                         {Path('manifest.json'),Path('features/cave_vein_choice.json')})
        choice=json.loads(new[Path('features/cave_vein_choice.json')])['minecraft:weighted_random_feature']
        self.assertEqual(choice['features'],
                         [[f'cavediamonds:cave_surface_vein_n{n}',weight]
                          for n,weight in ((1,1),(2,1),(3,25),(4,64),(5,10))])
        for n in range(1,6):
            feature=json.loads(new[Path(f'features/cave_surface_vein_n{n}.json')])['minecraft:aggregate_feature']
            expected=['cavediamonds:cave_select']
            if n>1: expected.append(f'cavediamonds:cave_ore_n{n-1}')
            self.assertEqual(feature['features'],expected)
            self.assertEqual(feature['early_out'],'none')

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'existing';target.mkdir()
            with self.assertRaises(FileExistsError): build_pack(target)


if __name__=='__main__': unittest.main()
