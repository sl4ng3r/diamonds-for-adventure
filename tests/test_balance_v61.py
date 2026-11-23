import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from tools.build_v61 import build_pack
from tools.build_v62 import build_pack as build_v62
from tools.build_v63 import DIST as V63_PACKAGE, VERSION as V63_VERSION, build_pack as build_v63

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'experiments/balance-v61/runtime/veins.js'


class V61BalanceTest(unittest.TestCase):
    @unittest.skipUnless(shutil.which('node'), 'node required for vein tests')
    def test_whole_vein_across_new_chunks_only_with_complete_landscape(self):
        script = f"""
            import assert from 'node:assert/strict';
            import {{readFileSync}} from 'node:fs';
            const source = readFileSync({json.dumps(str(SCRIPT))}, 'utf8');
            const {{planVeinRemoval}} = await import('data:text/javascript,' + encodeURIComponent(source));
            const seed = {{x:15,y:-57,z:8}};
            const other = {{x:16,y:-56,z:8}};
            const key = p => [p.x, p.y, p.z].join(',');
            const vein = new Map([seed, other].map(p => [key(p), 'minecraft:deepslate_diamond_ore']));
            const rightFace = key({{x:17,y:-56,z:8}});
            const read = (contact) => p => key(p) === rightFace ? contact
                : vein.get(key(p)) ?? 'minecraft:deepslate';
            const inSeedChunk = p => p.x < 16;
            const readyChunks = p => p.x < 32;
            const neverKeep = () => false;
            const plan = (contact, eligible) =>
                planVeinRemoval([seed], read(contact), inSeedChunk, neverKeep, eligible);
            assert.deepEqual(plan('minecraft:deepslate', readyChunks).map(r => r.position), [seed,other]);
            assert.deepEqual(plan('minecraft:deepslate', inSeedChunk), []);
            assert.deepEqual(plan('minecraft:air', readyChunks), []);
            assert.deepEqual(plan('minecraft:water', readyChunks), []);
            assert.deepEqual(plan(undefined, readyChunks), []);
        """
        subprocess.run(['node', '--input-type=module', '-e', script], cwd=ROOT, check=True)

    def test_cave_amendment_targets_deep_surfaces_and_preserves_ocean_rule(self):
        with TemporaryDirectory() as directory:
            pack = build_pack(Path(directory) / 'pack')
            original = ROOT / 'experiments/balance-v60/behavior_pack'
            for name in ('cave_upper_rule', 'cave_mid_rule', 'ocean_cave_rule', 'vein_pending_rule'):
                path = Path('feature_rules') / f'{name}.json'
                self.assertEqual((pack / path).read_bytes(), (original / path).read_bytes())
            path = pack / 'feature_rules/cave_abyss_rule.json'
            rule = json.loads(path.read_text())['minecraft:feature_rules']
            self.assertLessEqual(max(rule['distribution']['y']['extent']) + 4, -48)

    def test_v62_concentrates_additions_without_changing_the_vein_filter(self):
        with TemporaryDirectory() as directory:
            v61 = build_pack(Path(directory) / 'v61')
            v62 = build_v62(Path(directory) / 'v62')
            changed = {
                path.relative_to(v62).as_posix()
                for path in v62.rglob('*')
                if path.is_file() and path.read_bytes() != (v61 / path.relative_to(v62)).read_bytes()
            }
            self.assertEqual(changed, {
                'manifest.json', 'feature_rules/cave_abyss_rule.json', 'features/cave_abyss_chance.json',
            })
            rule = json.loads((v62 / 'feature_rules/cave_abyss_rule.json').read_text())
            distribution = rule['minecraft:feature_rules']['distribution']
            self.assertEqual(distribution['y']['extent'], [-54, -52])
            self.assertEqual(distribution['iterations'], 2)

    def test_v63_reduces_only_the_number_of_deep_placement_attempts(self):
        with TemporaryDirectory() as directory:
            v62 = build_v62(Path(directory) / 'v62')
            v63 = build_v63(Path(directory) / 'v63')
            rule = Path('feature_rules/cave_abyss_rule.json')
            changed = {
                path.relative_to(v63).as_posix()
                for path in v63.rglob('*')
                if path.is_file() and path.read_bytes() != (v62 / path.relative_to(v63)).read_bytes()
            }
            self.assertEqual(changed, {'manifest.json', rule.as_posix()})
            old = json.loads((v62 / rule).read_text())
            new = json.loads((v63 / rule).read_text())
            old['minecraft:feature_rules']['distribution']['iterations'] = 1
            self.assertEqual(new, old)

    def test_dist_contains_the_current_v63_generation(self):
        with TemporaryDirectory() as directory, ZipFile(V63_PACKAGE) as archive:
            pack = build_v63(Path(directory) / 'pack')
            files = {p.relative_to(pack).as_posix(): p
                     for p in pack.rglob('*') if p.is_file() and p.name != 'manifest.json'}
            self.assertIsNone(archive.testzip())
            self.assertEqual(set(archive.namelist()), set(files) | {'manifest.json', 'pack_icon.png'})
            for name, path in files.items():
                self.assertEqual(archive.read(name), path.read_bytes(), name)
            manifest = json.loads(archive.read('manifest.json'))
            original = json.loads((pack / 'manifest.json').read_text())
            self.assertEqual(manifest['header']['uuid'], original['header']['uuid'])
            self.assertEqual(manifest['header']['version'], list(V63_VERSION))
            self.assertEqual(manifest['dependencies'], original['dependencies'])
            self.assertEqual([m['version'] for m in manifest['modules']],
                             [list(V63_VERSION)] * len(original['modules']))
