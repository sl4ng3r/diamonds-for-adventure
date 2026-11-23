import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from tools.build_v57_dist import build_package


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v57/behavior_pack'


class V57DistPackageTest(unittest.TestCase):
    def test_fixed_package_preserves_v57_generation(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            zipfile.ZipFile(build_package(Path(directory) / 'historical.mcpack')) as archive,
        ):
            self.assertIsNone(archive.testzip())
            source_files = {p.relative_to(SOURCE).as_posix(): p.read_bytes()
                            for p in SOURCE.rglob('*') if p.is_file()}
            self.assertEqual(set(archive.namelist()), set(source_files) | {'pack_icon.png'})
            for name, data in source_files.items():
                if name != 'manifest.json':
                    self.assertEqual(archive.read(name), data, name)
            manifest = json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['header']['name'], 'Cave Diamonds')
            self.assertEqual(manifest['header']['version'], [0, 1, 9])
            self.assertEqual(manifest['header']['uuid'],
                             json.loads(source_files['manifest.json'])['header']['uuid'])
            self.assertEqual([module['version'] for module in manifest['modules']],
                             [[0, 1, 9]] * len(manifest['modules']))

    def test_builder_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'existing.mcpack'
            target.write_bytes(b'keep')
            with self.assertRaises(FileExistsError):
                build_package(target)
            self.assertEqual(target.read_bytes(), b'keep')

    def test_next_release_changes_only_manifest_version(self):
        with (
            tempfile.TemporaryDirectory() as directory,
            zipfile.ZipFile(build_package(Path(directory) / 'previous.mcpack')) as old,
            zipfile.ZipFile(build_package(Path(directory) / 'following.mcpack', version=[0, 1, 10])) as new,
        ):
            self.assertIsNone(new.testzip())
            self.assertEqual(set(new.namelist()), set(old.namelist()))
            for name in old.namelist():
                if name != 'manifest.json':
                    self.assertEqual(new.read(name), old.read(name), name)
            old_manifest = json.loads(old.read('manifest.json'))
            new_manifest = json.loads(new.read('manifest.json'))
            self.assertEqual(new_manifest['header']['version'], [0, 1, 10])
            self.assertEqual(
                [module['version'] for module in new_manifest['modules']],
                [[0, 1, 10]] * len(new_manifest['modules']),
            )
            new_manifest['header']['version'] = old_manifest['header']['version']
            for old_module, new_module in zip(old_manifest['modules'], new_manifest['modules']):
                new_module['version'] = old_module['version']
            self.assertEqual(new_manifest, old_manifest)

    def test_builder_supports_next_release_without_overwriting_previous(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'next.mcpack'
            build_package(target, version=[0, 1, 10])
            with zipfile.ZipFile(target) as archive:
                manifest = json.loads(archive.read('manifest.json'))
            self.assertEqual(manifest['header']['version'], [0, 1, 10])


if __name__ == '__main__':
    unittest.main()
