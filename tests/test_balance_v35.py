import json
import tempfile
import unittest
from pathlib import Path

from tools.build_v35 import build_pack


ROOT = Path(__file__).resolve().parents[1]
V29 = ROOT / 'experiments/balance-v29/behavior_pack'
V35 = ROOT / 'experiments/balance-v35/behavior_pack'


class BalanceV35Test(unittest.TestCase):
    def test_surface_rules_preserved_and_ore_veins_replace_flat_patterns(self):
        old = {p.relative_to(V29): p.read_bytes() for p in V29.rglob('*') if p.is_file()}
        new = {p.relative_to(V35): p.read_bytes() for p in V35.rglob('*') if p.is_file()}
        self.assertEqual(set(old) - set(new), set())
        self.assertEqual(set(new) - set(old),
                         {Path(f'features/cave_ore_n{size}.json') for size in range(1,6)})
        self.assertEqual({name for name in old if old[name] != new[name]},
                         {Path('manifest.json'),Path('features/cave_vein_choice.json')})
        choice=json.loads(new[Path('features/cave_vein_choice.json')])['minecraft:weighted_random_feature']
        self.assertEqual(choice['features'],
                         [[f'cavediamonds:cave_ore_n{size}',weight]
                          for size,weight in ((1,1),(2,1),(3,25),(4,64),(5,10))])
        for size in range(1,6):
            ore=json.loads(new[Path(f'features/cave_ore_n{size}.json')])['minecraft:ore_feature']
            self.assertEqual(ore['count'],size)
            self.assertEqual(ore['replace_rules'],[
                {'places_block':'minecraft:diamond_ore','may_replace':['minecraft:stone']},
                {'places_block':'minecraft:deepslate_diamond_ore','may_replace':['minecraft:deepslate']},
            ])

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'existing'
            target.mkdir()
            with self.assertRaises(FileExistsError):
                build_pack(target)


if __name__=='__main__':
    unittest.main()
