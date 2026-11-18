"""Add rare buried diamonds above Y=-20 to the V44 cave balance."""

import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/balance-v45/behavior_pack'
V44 = ROOT / 'experiments/balance-v44/behavior_pack'
RULE_SOURCE = ROOT / 'experiments/balance-v37/behavior_pack/feature_rules/sparse_buried_rule.json'
TARGET = ROOT / 'experiments/balance-v46/behavior_pack'


def build_pack(target=TARGET):
    target = Path(target)
    shutil.copytree(SOURCE, target)
    shutil.copy2(V44 / 'features/diamond_ore_buried_feature.json',
                 target / 'features/diamond_ore_buried_feature.json')

    rule = json.loads(RULE_SOURCE.read_text())
    body = rule['minecraft:feature_rules']
    body['description']['identifier'] = 'cavediamonds:upper_buried_rule'
    body['distribution']['iterations'] = 1
    body['distribution']['y']['extent'] = [-19, 16]
    (target / 'feature_rules/upper_buried_rule.json').write_text(
        json.dumps(rule, ensure_ascii=False, indent=2) + '\n'
    )

    manifest_path = target / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['header']['name'] = 'Cave Diamonds – V46 Upper Buried Experiment'
    manifest['header']['description'] = (
        'Forschungsvariante: eingeschlossene Erzadern oberhalb von Y=-20; nicht freigegeben'
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return target


def main():
    print(build_pack())


if __name__ == '__main__':
    main()
