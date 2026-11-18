"""Compare buried ore deposits above Y=-20 using frozen Vanilla scans."""

import argparse
import json
from pathlib import Path

from tools.balance_batch import inspect_results
from tools.balance_experiment import ROOT
from tools.balance_followup import load_plan
from tools.vanilla_reference import DIRECTIONS, FLUIDS


def buried_metrics(ores, low=-19, high=16):
    positions = {
        (ore['x'], ore['y'], ore['z']) for ore in ores
        if low <= ore['y'] <= high
        and 'minecraft:air' not in ore['neighbours']
        and not any(block in FLUIDS for block in ore['neighbours'])
    }
    remaining = set(positions)
    groups = 0
    while remaining:
        stack = [remaining.pop()]
        groups += 1
        while stack:
            x, y, z = stack.pop()
            for dx, dy, dz in DIRECTIONS:
                neighbor = (x + dx, y + dy, z + dz)
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    stack.append(neighbor)
    return {'blocks': len(positions), 'groups': groups, 'positions': positions}


def summarize_plans(plans):
    totals = {'vanilla_blocks': 0, 'candidate_blocks': 0,
              'vanilla_groups': 0, 'candidate_groups': 0,
              'vanilla_positions_retained': 0, 'areas': 0, 'chunks': 0}
    for plan_path in plans:
        pack, results, reference = load_plan(Path(plan_path))
        status = inspect_results(pack, results, reference)
        if status['missing']:
            raise ValueError(f'incomplete plan {plan_path}: {status["missing"]}')
        for index in status['completed']:
            row = json.loads((results / f'area-{index:02d}.json').read_text())
            vanilla_path = (ROOT / row['reference_world_scan']).resolve()
            candidate_path = (ROOT / row['candidate_world'] / 'ore_scan.json').resolve()
            research = (ROOT / 'data/research').resolve()
            if not vanilla_path.is_relative_to(research) or not candidate_path.is_relative_to(research):
                raise ValueError('scan path must stay in data/research')
            vanilla = buried_metrics(json.loads(vanilla_path.read_text())['ores'])
            candidate = buried_metrics(json.loads(candidate_path.read_text())['ores'])
            for side, value in (('vanilla', vanilla), ('candidate', candidate)):
                totals[f'{side}_blocks'] += value['blocks']
                totals[f'{side}_groups'] += value['groups']
            totals['vanilla_positions_retained'] += len(vanilla['positions'] & candidate['positions'])
            totals['areas'] += 1
            totals['chunks'] += row['chunks_per_side'] ** 2
    for key in ('blocks', 'groups'):
        base = totals[f'vanilla_{key}']
        totals[f'{key}_percent_of_vanilla'] = round(100 * totals[f'candidate_{key}'] / base, 1) if base else None
    return totals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', action='append', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(summarize_plans(args.plan), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
