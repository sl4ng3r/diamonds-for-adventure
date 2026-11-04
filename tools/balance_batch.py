#!/usr/bin/env python3
"""Resume disposable-world balance scans and print a small, non-release status."""
import argparse
import hashlib
import json
from pathlib import Path

from tools.balance_experiment import REFERENCE, pack_digest, read_reference, scan_area, summarize
from tools.balance_profiles import exposure_profile


def ratio(value, baseline):
    return round(100 * value / baseline, 1) if baseline else None


def inspect_results(pack, results, reference):
    areas = read_reference(reference)['areas']
    digest = pack_digest(pack)
    ref_digest = hashlib.sha256(reference.read_bytes()).hexdigest()
    found = set()
    for path in sorted(results.glob('area-*.json')):
        data = json.loads(path.read_text())
        index = data.get('index')
        if type(index) is not int or not 0 <= index < len(areas) or path.name != f'area-{index:02d}.json' or index in found:
            raise ValueError(f'invalid or duplicate result index: {path}')
        if data.get('pack_sha256') != digest or data.get('reference_sha256') != ref_digest:
            raise ValueError(f'pack or reference mismatch: {path}')
        for field in ('seed', 'chunk_x', 'chunk_z', 'chunks_per_side'):
            if data.get(field) != areas[index][field]:
                raise ValueError(f'{field} does not match reference: {path}')
        found.add(index)
    return {'completed': sorted(found), 'missing': [i for i in range(len(areas)) if i not in found],
            'total': len(areas), 'pack_sha256': digest, 'reference_sha256': ref_digest}


def run_pending(pack, results, reference, limit=None):
    if limit is not None and limit < 1:
        raise ValueError('limit must be positive')
    status = inspect_results(pack, results, reference)
    for index in status['missing'][:limit]:
        scan_area(pack, results, index, reference)
    return inspect_results(pack, results, reference)


def exposure_summary(results):
    from tools.balance_experiment import ROOT
    output={'vanilla': None, 'candidate': None, 'candidate_upper_17_to_40': None}
    areas=[json.loads(p.read_text()) for p in sorted(results.glob('area-*.json'))]
    if not areas: return output
    for side in ('vanilla','candidate'):
        profiles=[]
        for area in areas:
            scan_path=(ROOT/area['reference_world_scan'] if side=='vanilla' and 'reference_world_scan' in area
                       else ROOT/area['candidate_world']/'ore_scan.json' if side=='candidate' and 'candidate_world' in area else None)
            if scan_path is None or not scan_path.is_file(): break
            profiles.append(exposure_profile(json.loads(scan_path.read_text())))
        if len(profiles)==len(areas):
            output[side]={key:sum(p[key] for p in profiles) for key in ('air_exposed','floor','wall','ceiling','only_floor','only_wall','only_ceiling')}
            output[side]['air_by_height']={band:sum(p['air_by_height'][band] for p in profiles) for band in profiles[0]['air_by_height']}
    if all('candidate_upper_diamonds_17_to_40' in a for a in areas):
        output['candidate_upper_17_to_40']=sum(a['candidate_upper_diamonds_17_to_40'] for a in areas)
    output['note']='Counts overlap when an ore touches air on multiple faces; air contact does not prove accessibility. Upper scan covers Y=17..40 only; null means not scanned.'
    return output


def surface_probe_summary(path, digest):
    if not path.is_file(): return None
    data=json.loads(path.read_text())
    if data['pack_sha256']!=digest: raise ValueError(f'surface probe pack mismatch: {path}')
    output={}
    for probe in data['probes']:
        entry=output.setdefault(probe['surface'],{'attempts':0,'on_face':0})
        entry['attempts']+=1
        if probe['placed'] and probe['ore_on_face']>0: entry['on_face']+=1
    return output


def compact_status(pack, results, reference):
    status = inspect_results(pack, results, reference)
    status['surface_probes']=surface_probe_summary(results.parent/'verification/surface-probes.json',status['pack_sha256'])
    if status['completed']:
        report = summarize(results, reference)
        v = report['vanilla']['totals']
        c = report['candidate']['totals']
        def metric(a, b):
            return {'vanilla': a, 'candidate': b, 'percent_of_vanilla': ratio(b, a)}
        status['measurements'] = {
            'air_adjacent_groups': metric(v['deposits']['air_adjacent'], c['deposits']['air_adjacent']),
            'buried_y_minus57': metric(v['y_minus57']['buried'], c['y_minus57']['buried']),
            'buried_y_minus59_to_minus55': metric(v['tunnel_band']['buried'], c['tunnel_band']['buried']),
            'model_tunnel_contacts': metric(report['tunnel_contacts']['vanilla'], report['tunnel_contacts']['candidate']),
        }
        status['exposure'] = exposure_summary(results)
    status['limitations'] = ('No release decision: small or selected samples, air contact is not cave access; '
                             'tunnel contacts are overlapping models, not measured player yield. '
                             'Ore size, other blocks, persistence, performance and Realm require separate tests.')
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('status', 'run'))
    parser.add_argument('--pack', type=Path, required=True)
    parser.add_argument('--results', type=Path, required=True)
    parser.add_argument('--reference', type=Path, default=REFERENCE)
    parser.add_argument('--limit', type=int, help='maximum number of missing areas to run')
    args = parser.parse_args()
    if not args.pack.is_dir() or not (args.pack / 'manifest.json').is_file():
        parser.error('pack must be an existing behavior pack with manifest.json')
    if args.command == 'status' and args.limit is not None:
        parser.error('--limit applies only to run')
    if args.command == 'run':
        run_pending(args.pack.resolve(), args.results, args.reference, args.limit)
    print(json.dumps(compact_status(args.pack.resolve(), args.results, args.reference), ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    main()
