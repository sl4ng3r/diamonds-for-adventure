import json
import struct
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'experiments/balance-v26/behavior_pack'
PACKAGE = ROOT / 'experiments/balance-v26-icon/cave-diamonds-v26-icon-test.mcpack'
RELEASE = ROOT / 'experiments/balance-v26-icon/cave-diamonds-v0.1.2.mcpack'


class V26IconPackageTest(unittest.TestCase):
    def test_package_preserves_world_generation_and_pack_identity(self):
        with zipfile.ZipFile(PACKAGE) as archive:
            self.assertIsNone(archive.testzip())
            original = json.loads((ORIGINAL / 'manifest.json').read_text())
            manifest = json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['header']['uuid'], original['header']['uuid'])
            self.assertGreater(manifest['header']['version'], original['header']['version'])
            original['header']['version'] = [0, 1, 1]
            for module in original['modules']:
                module['version'] = [0, 1, 1]
            self.assertEqual(manifest, original)
            self.assertEqual(manifest['modules'][0]['uuid'], original['modules'][0]['uuid'])
            self.assertEqual(manifest['modules'][0]['version'], manifest['header']['version'])
            self.assertEqual({m['type'] for m in manifest['modules']}, {'data'})
            self.assertFalse(manifest.get('dependencies'))
            for directory in ('features', 'feature_rules'):
                expected = {p.relative_to(ORIGINAL).as_posix() for p in (ORIGINAL / directory).rglob('*') if p.is_file()}
                actual = {n for n in archive.namelist() if n.startswith(directory + '/') and not n.endswith('/')}
                self.assertEqual(actual, expected)
                for name in expected:
                    self.assertEqual(archive.read(name), (ORIGINAL / name).read_bytes(), name)

    def test_icon_is_square_png_at_pack_root(self):
        with zipfile.ZipFile(PACKAGE) as archive:
            data = archive.read('pack_icon.png')
        self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
        self.assertEqual(data[12:16], b'IHDR')
        self.assertEqual(struct.unpack('>II', data[16:24]), (256, 256))

    def test_release_is_same_gameplay_with_clean_name_and_new_version(self):
        with zipfile.ZipFile(PACKAGE) as old, zipfile.ZipFile(RELEASE) as new:
            self.assertIsNone(new.testzip())
            self.assertEqual(set(old.namelist()), set(new.namelist()))
            for name in old.namelist():
                if name != 'manifest.json':
                    self.assertEqual(old.read(name), new.read(name), name)
            original = json.loads(old.read('manifest.json'))
            manifest = json.loads(new.read('manifest.json'))
            original['header']['name'] = 'Cave Diamonds'
            original['header']['description'] = 'Diamanten in Höhlen entdecken und seltener in tiefem Gestein finden.'
            original['header']['version'] = [0, 1, 2]
            for module in original['modules']:
                module['version'] = [0, 1, 2]
            self.assertEqual(manifest, original)


if __name__ == '__main__':
    unittest.main()
