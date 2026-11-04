#!/usr/bin/env python3
"""Match the predetermined holdout areas to unique vanilla scan files."""
import json
import argparse
from pathlib import Path
import subprocess
import sys
from tools.compare_worlds import ROOT, PACK_ID

PLAN=ROOT/'reference/balance-holdout-plan-2026-11-04.json'
OUTPUT=ROOT/'reference/balance-holdout-1.26.61.1-2026-11-04.json'
INPUTS=ROOT/'reference/balance-holdout-1.26.61.1-2026-11-04-inputs.txt'

def match_plan(plan, reports):
    result=[]
    for area in plan['areas']:
        matches=[path for path,report in reports if all(report[k]==area[k] for k in ('seed','chunk_x','chunk_z')) and report['chunks_per_side']==plan['chunks_per_side']]
        if len(matches)!=1: raise ValueError(f'expected exactly one vanilla scan for {area}, found {len(matches)}')
        result.append(matches[0])
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan',type=Path,default=PLAN)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--inputs',type=Path,default=INPUTS)
    parser.add_argument('--measurement-date',default='2026-11-04')
    args=parser.parse_args()
    if args.output.exists() or args.inputs.exists(): raise FileExistsError('holdout output already exists; preserve it')
    plan=json.loads(args.plan.read_text())
    reports=[]
    for path in (ROOT/'data/research').glob('cavediamonds-research-*/vanilla_reference.json'):
        report=json.loads(path.read_text())
        reports.append((path,report))
    selected=match_plan(plan,reports)
    for path in selected:
        log=(path.parent/'server.log').read_text(errors='replace')
        if 'Version: '+plan['server_version'] not in log or any(PACK_ID in line and 'Pack Stack' in line for line in log.splitlines()):
            raise ValueError(f'version or vanilla validation failed: {path}')
    relative=[str(path.relative_to(ROOT)) for path in selected]
    subprocess.run([sys.executable,'-m','tools.aggregate_vanilla_reference','--server-version',plan['server_version'],
                    '--measurement-date',args.measurement_date,'--output',str(args.output),*relative],cwd=ROOT,check=True)
    with args.inputs.open('x') as f: f.write('\n'.join(relative)+'\n')
    print(f'Holdout input list: {args.inputs}')

if __name__=='__main__': main()
