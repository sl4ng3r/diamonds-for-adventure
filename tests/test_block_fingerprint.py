import shutil
import subprocess
import unittest
from pathlib import Path


@unittest.skipUnless(shutil.which('node'), 'node required for diagnostic JavaScript test')
class BlockFingerprintTests(unittest.TestCase):
    def test_ore_is_normalized_but_other_block_changes_affect_hash(self):
        script = r'''
import { updateFingerprint } from './diagnostics/behavior_pack/scripts/block_fingerprint.js';
const h=2166136261;
if (updateFingerprint(h,'minecraft:diamond_ore') !== updateFingerprint(h,'minecraft:stone')) process.exit(1);
if (updateFingerprint(h,'minecraft:deepslate_diamond_ore') !== updateFingerprint(h,'minecraft:deepslate')) process.exit(2);
if (updateFingerprint(h,'minecraft:water') === updateFingerprint(h,'minecraft:air')) process.exit(3);
'''
        subprocess.run(['node', '--input-type=module', '-e', script], cwd=Path(__file__).resolve().parents[1], check=True)
