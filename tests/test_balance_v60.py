import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest

from tools.build_v60 import build_pack

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'experiments/balance-v60/runtime/veins.js'


class VeinThinningTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'node required for vein tests')
    def test_surfaces_and_incomplete_veins_are_preserved_as_whole_groups(self):
        script = f"""
            import assert from 'node:assert/strict';
            import {{readFileSync}} from 'node:fs';
            const source = readFileSync({json.dumps(str(SCRIPT))}, 'utf8');
            const {{planVeinRemoval}} = await import('data:text/javascript,' + encodeURIComponent(source));
            const point = (x, y, z) => ({{x, y, z}});
            const key = p => [p.x, p.y, p.z].join(',');
            const ore = 'minecraft:deepslate_diamond_ore';
            const stone = 'minecraft:stone';
            const vein = [point(5,-40,4), point(6,-40,4), point(7,-39,4)];
            function check(seeds, extra, result, contains = () => true, keep = () => false) {{
                const world = new Map(seeds.map(p => [key(p), ore]));
                for (const [p, block] of extra) world.set(key(p), block);
                const read = p => world.has(key(p)) ? world.get(key(p)) : stone;
                const classified = planVeinRemoval(seeds, read, contains, keep);
                assert.deepEqual(classified.map(p => key(p.position)).sort(), result.map(key).sort());
            }}
            check(vein, [[point(8,-39,4), 'minecraft:air']], []);
            check(vein, [[point(8,-39,4), 'minecraft:water']], []);
            check(vein, [[point(8,-39,4), undefined]], []);
            check(vein, [], [], p => p.x < 7);
            check(vein, [], [], () => true, () => true);
            check(vein, [], vein);
            const highEdge = [point(5,16,4), point(5,17,4)];
            check(highEdge, [], []);
        """
        subprocess.run(['node', '--input-type=module', '-e', script], cwd=ROOT, check=True)

    def test_runtime_replaces_the_block_filters_and_retains_ocean_generation(self):
        with TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'pack')
            rules = pack / 'feature_rules'
            for name in ('thin_overworld', 'thin_upper_overworld'):
                self.assertFalse((rules / (name + '.json')).exists())
            self.assertFalse((pack / 'features/diamond_ore_buried_feature.json').exists())
            old_ocean_rule = ROOT / 'experiments/balance-v59/behavior_pack/feature_rules/ocean_cave_rule.json'
            self.assertEqual((rules / old_ocean_rule.name).read_bytes(), old_ocean_rule.read_bytes())
            manifest = json.loads((pack / 'manifest.json').read_text())
            script = next(module for module in manifest['modules'] if module['type'] == 'script')
            self.assertTrue((pack / script['entry']).is_file())
