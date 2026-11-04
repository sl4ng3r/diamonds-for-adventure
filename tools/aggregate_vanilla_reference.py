#!/usr/bin/env python3
"""Build a reproducible summary from explicitly selected vanilla scan files."""
import argparse
import json
from pathlib import Path
from tools.vanilla_reference import aggregate, analyze


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--overwrite',action='store_true',help='explicitly replace an existing generated summary')
    parser.add_argument('--server-version',required=True,help='verified server version for these scans')
    parser.add_argument('--measurement-date',required=True,help='date the worlds were scanned, YYYY-MM-DD')
    parser.add_argument('reports',type=Path,nargs='+')
    args=parser.parse_args()
    reports=[]
    for report_path in args.reports:
        original=json.loads(report_path.read_text())
        scan_path=report_path.parent/'ore_scan.json'
        scan=json.loads(scan_path.read_text())
        n=original['chunks_per_side']
        summary=analyze(scan,original['chunk_x']*16,original['chunk_z']*16,n*16)
        reports.append({'seed':original['seed'],'chunk_x':original['chunk_x'],'chunk_z':original['chunk_z'],
                        'chunks_per_side':n,'scan_file':str(scan_path),**summary})
    result={'server_version':args.server_version,'measurement_date':args.measurement_date,
            'range_y':[-64,16],'note':'Vanilla, selected areas; air adjacency is not proof of accessible caves. Connected components use faces and may be truncated at scan boundaries.',
            **aggregate(reports),'areas':reports}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    if args.output.exists() and not args.overwrite: raise FileExistsError(f'refusing to overwrite {args.output}')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'regions':result['regions'],'seeds':result['seeds'],
                      'total_chunks':result['total_chunks'],'totals':result['totals']},indent=2))

if __name__=='__main__': main()
