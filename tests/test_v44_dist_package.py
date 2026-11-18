import json
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build_v44_dist import build_package


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v44/behavior_pack'
ICON = ROOT / 'experiments/balance-v26-icon/pack_icon.png'
PACKAGE = ROOT / 'dist/cave-diamonds-v0.1.6.mcpack'


class V44DistPackageTest(unittest.TestCase):
    def test_versioned_package_preserves_v44_generation(self):
        with zipfile.ZipFile(PACKAGE) as archive:
            self.assertIsNone(archive.testzip())
            source_files = {
                path.relative_to(SOURCE).as_posix(): path.read_bytes()
                for path in SOURCE.rglob('*') if path.is_file()
            }
            self.assertEqual(set(archive.namelist()), set(source_files) | {'pack_icon.png'})
            for name, content in source_files.items():
                if name != 'manifest.json':
                    self.assertEqual(archive.read(name), content, name)

            original = json.loads(source_files['manifest.json'])
            manifest = json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['header']['uuid'], original['header']['uuid'])
            self.assertEqual(manifest['header']['version'], [0, 1, 6])
            self.assertEqual(manifest['header']['name'], 'Cave Diamonds')
            self.assertNotIn('test', manifest['header']['description'].lower())
            self.assertEqual(
                [module['version'] for module in manifest['modules']],
                [[0, 1, 6]] * len(manifest['modules']),
            )
            original['header']['name'] = manifest['header']['name']
            original['header']['description'] = manifest['header']['description']
            original['header']['version'] = [0, 1, 6]
            for module in original['modules']:
                module['version'] = [0, 1, 6]
            self.assertEqual(manifest, original)

            icon = archive.read('pack_icon.png')
            self.assertEqual(icon, ICON.read_bytes())
            self.assertEqual(icon[:8], b'\x89PNG\r\n\x1a\n')
            self.assertEqual(icon[12:16], b'IHDR')
            self.assertEqual(struct.unpack('>II', icon[16:24]), (256, 256))

    def test_builder_refuses_to_replace_existing_package(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing.mcpack'
            target.write_bytes(b'keep')
            with self.assertRaises(FileExistsError):
                build_package(target)
            self.assertEqual(target.read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
