import json
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build_v29_playtest import build_package


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v29/behavior_pack'
ICON = ROOT / 'experiments/balance-v26-icon/pack_icon.png'
PACKAGE = ROOT / 'experiments/balance-v29/cave-diamonds-v29-playtest.mcpack'


class V29PlaytestPackageTest(unittest.TestCase):
    def test_package_has_new_version_and_identical_generation_files(self):
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

            source_manifest = json.loads(source_files['manifest.json'])
            manifest = json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['header']['uuid'], source_manifest['header']['uuid'])
            self.assertEqual(manifest['header']['version'], [0, 1, 3])
            self.assertEqual(manifest['header']['name'], 'Cave Diamonds')
            self.assertIn('Test', manifest['header']['description'])
            self.assertEqual(
                [module['version'] for module in manifest['modules']],
                [[0, 1, 3]] * len(manifest['modules']),
            )
            source_manifest['header']['name'] = manifest['header']['name']
            source_manifest['header']['description'] = manifest['header']['description']
            source_manifest['header']['version'] = [0, 1, 3]
            for module in source_manifest['modules']:
                module['version'] = [0, 1, 3]
            self.assertEqual(manifest, source_manifest)

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
