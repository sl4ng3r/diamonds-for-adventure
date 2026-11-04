import shutil
import subprocess
import unittest
from pathlib import Path


@unittest.skipUnless(shutil.which('node'), 'node required for diagnostic JavaScript test')
class AirProbeTests(unittest.TestCase):
    def test_small_large_and_boundary_components(self):
        root = Path(__file__).resolve().parents[1]
        script = r'''
import { probeAir } from './diagnostics/behavior_pack/scripts/air_probe.js';
const bounds={minX:0,maxX:9,minY:0,maxY:9,minZ:0,maxZ:9};
const one = p => p.x===5 && p.y===5 && p.z===5 ? 'minecraft:air':'minecraft:stone';
const air = () => 'minecraft:air';
const small=probeAir({x:5,y:5,z:5},one,bounds,64);
const large=probeAir({x:5,y:5,z:5},air,bounds,64);
const boundary=probeAir({x:0,y:0,z:0},p => p.x===0 && p.y===0 && p.z===0 ? 'minecraft:air':'minecraft:stone',bounds,64);
if (small.status!=='small' || small.count!==1 || large.status!=='large' || boundary.status!=='boundary') process.exit(1);
'''
        subprocess.run(['node', '--input-type=module', '-e', script], cwd=root, check=True)
