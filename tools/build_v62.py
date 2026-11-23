"""Focus V61's additional cave attempts on the deepest air in the calibration regions."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.build_v57_dist import build_package
from tools.build_v59 import ROOT, write_json
from tools.build_v61 import build_pack as build_v61


TARGET = ROOT / 'experiments/balance-v62/behavior_pack'
VERSION = (0, 1, 15)
DIST = ROOT / 'dist/cave-diamonds-v0.1.15.mcpack'


def build_pack(target=TARGET):
    target = build_v61(target, deep_start=(-54, -52), deep_attempts=2, deep_chance=65)
    path = target / 'manifest.json'
    manifest = json.loads(path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V62 Deep Caves'
    write_json(path, manifest)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', action='store_true', help=f'Build {DIST.name}')
    if parser.parse_args().package:
        with TemporaryDirectory() as directory:
            print(build_package(DIST, VERSION, source=build_pack(Path(directory) / 'behavior_pack')))
    else:
        print(build_pack())


if __name__ == '__main__':
    main()
