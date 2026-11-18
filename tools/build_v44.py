"""Build V44 with sparse new cave sites beside preserved Vanilla cave diamonds."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v43/behavior_pack'
RULE_SOURCE = ROOT / 'experiments/balance-v37/behavior_pack/feature_rules'
TARGET = ROOT / 'experiments/balance-v44/behavior_pack'
RULES = (('cave_rule', 10), ('cave_mid_rule', 15))


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    for name, chance in RULES:
        rule = json.loads((RULE_SOURCE / f'{name}.json').read_text())
        rule['minecraft:feature_rules']['distribution']['scatter_chance'] = chance
        (target / f'feature_rules/{name}.json').write_text(
            json.dumps(rule, ensure_ascii=False, indent=2) + '\n'
        )
    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V44 Vanilla Plus Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante: Vanilla-Höhlenadern plus wenige neue Fundstellen; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
