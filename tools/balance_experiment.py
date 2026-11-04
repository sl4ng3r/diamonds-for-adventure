#!/usr/bin/env python3
"""Build and measure a non-release balance candidate in disposable worlds."""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from tools.compare_worlds import (ROOT, count_tunnel_finds, create_combined_generation_variant,
                                  eula_accepted, run, set_snap_selection)
from tools.vanilla_reference import aggregate, analyze

REFERENCE=ROOT/'reference/vanilla-1.26.61.1-2026-11-03.json'

def write_result_once(path, result):
    # Atomic publish in the same directory; link fails instead of overwriting.
    temp_path=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.pending-',delete=False) as out:
            temp_path=Path(out.name)
            json.dump(result,out,indent=2); out.write('\n')
        os.link(temp_path,path)
    finally:
        if temp_path is not None: temp_path.unlink(missing_ok=True)

def pack_digest(pack):
    digest=hashlib.sha256()
    for path in sorted(p for p in pack.rglob('*') if p.is_file()):
        name=path.relative_to(pack).as_posix().encode()
        content=path.read_bytes()
        digest.update(len(name).to_bytes(8,'big')); digest.update(name)
        digest.update(len(content).to_bytes(8,'big')); digest.update(content)
    return digest.hexdigest()

def diff_ore_trace(before, after):
    first = {tuple(row) for row in before['oreTrace']}
    second = {tuple(row) for row in after['oreTrace']}
    return {'removed': [list(row) for row in sorted(first - second)],
            'added': [list(row) for row in sorted(second - first)]}

def evaluate_mining(before, after, mined):
    def records(scan):
        return {(o['x'],o['y'],o['z']):o['type'] for o in scan['ores']}
    a,b=records(before),records(after)
    target=(mined['x'],mined['y'],mined['z'])
    chunk=(target[0]//16,target[2]//16)
    other_positions=(a.keys()|b.keys())-{target}
    changes=[p for p in other_positions if a.get(p)!=b.get(p)]
    return {'mined_ore_reappeared':target in b,
            'other_changes_modified_chunk':sum((p[0]//16,p[2]//16)==chunk for p in changes),
            'changes_other_chunks':sum((p[0]//16,p[2]//16)!=chunk for p in changes)}

def create_candidate(source, destination, profile='v1'):
    # Copy to a new path only: never modify the original prototype or a world.
    if profile not in ('v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19'): raise ValueError('unknown experimental profile')
    pack=create_combined_generation_variant(source,destination)
    set_snap_selection(pack,'floor')
    cave_path=pack/'feature_rules/cave_rule.json'
    cave=json.loads(cave_path.read_text())
    cave['minecraft:feature_rules']['distribution']['iterations']={'v1':1,'v2':2,'v3':3,'v4':4,'v5':3,'v6':3,'v7':2,'v8':2,'v9':2,'v10':1,'v11':1,'v12':1,'v13':1,'v14':1,'v15':1,'v16':2,'v17':1,'v18':1,'v19':1}[profile]
    cave_path.write_text(json.dumps(cave,indent=2)+'\n')
    if profile=='v6':
        extra=json.loads(json.dumps(cave))
        rule=extra['minecraft:feature_rules']
        rule['description']['identifier']='cavediamonds:cave_extra_rule'
        rule['distribution']['iterations']=1
        rule['distribution']['scatter_chance']=30
        (pack/'feature_rules/cave_extra_rule.json').write_text(json.dumps(extra,indent=2)+'\n')
    snap_path=pack/'features/cave_snap_floor.json'
    snap=json.loads(snap_path.read_text())
    snap['minecraft:snap_to_surface_feature']['allow_underwater_placement']=False
    if profile in ('v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19'):
        def feature(name,kind,body):
            (pack/'features'/(name+'.json')).write_text(json.dumps({'format_version':'1.21.40',kind:{'description':{'identifier':'cavediamonds:'+name},**body}},indent=2)+'\n')
        choices=[]
        for name,dx,dy,dz in [('east',1,0,0),('west',-1,0,0),('north',0,0,-1),('south',0,0,1),('down',0,-1,0)]:
            identifier='cave_neighbor_'+name
            feature(identifier,'minecraft:scatter_feature',{'places_feature':'cavediamonds:cave_select','distribution':{'iterations':1,'x':dx,'y':dy,'z':dz}})
            choices.append(['cavediamonds:'+identifier,1])
        feature('cave_neighbor_choice','minecraft:weighted_random_feature',{'features':choices})
        feature('cave_neighbor_chance','minecraft:scatter_feature',{'places_feature':'cavediamonds:cave_neighbor_choice','distribution':{'iterations':1,'scatter_chance':70 if profile=='v5' else 40,'x':0,'y':0,'z':0}})
        feature('cave_pair','minecraft:aggregate_feature',{'features':['cavediamonds:cave_select','cavediamonds:cave_neighbor_chance'],'early_out':'none'})
        snap['minecraft:snap_to_surface_feature']['feature_to_snap']='cavediamonds:cave_pair'
        if profile=='v9':
            neighbors=['cavediamonds:cave_neighbor_east','cavediamonds:cave_neighbor_west','cavediamonds:cave_neighbor_north','cavediamonds:cave_neighbor_south']
            for n in range(1,6):
                feature(f'cave_vein_{n}','minecraft:aggregate_feature',{'features':['cavediamonds:cave_select']+neighbors[:n-1],'early_out':'none'})
            feature('cave_vein_choice','minecraft:weighted_random_feature',{'features':[[f'cavediamonds:cave_vein_{n}',weight] for n,weight in [(1,5),(2,15),(3,35),(4,35),(5,10)]]})
            snap['minecraft:snap_to_surface_feature']['feature_to_snap']='cavediamonds:cave_vein_choice'
        if profile in ('v10','v11','v12','v13','v14','v15','v16','v17','v18','v19'):
            directions=['east','north','west','south','down'] if profile=='v10' else ['east','north','west','south']
            size_weights={1:5,2:15,3:35,4:35,5:10}
            choices=[]
            orders=[directions[rotation:]+directions[:rotation] for rotation in range(len(directions))]
            if profile in ('v11','v12','v16','v17','v18','v19'):
                orders += [list(reversed(order)) for order in orders]
            for rotation,order in enumerate(orders):
                refs=['cavediamonds:cave_neighbor_'+name for name in order]
                for size,weight in size_weights.items():
                    name=f'cave_vein_r{rotation}_n{size}'
                    feature(name,'minecraft:aggregate_feature',{'features':['cavediamonds:cave_select']+refs[:size-1],'early_out':'none'})
                    choices.append([f'cavediamonds:{name}',weight])
            feature('cave_vein_choice','minecraft:weighted_random_feature',{'features':choices})
            snap['minecraft:snap_to_surface_feature']['feature_to_snap']='cavediamonds:cave_vein_choice'
    snap_path.write_text(json.dumps(snap,indent=2)+'\n')
    if profile in ('v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19'):
        for surface in ('ceiling','wall'):
            surface_doc=json.loads(json.dumps(snap))
            surface_body=surface_doc['minecraft:snap_to_surface_feature']
            surface_body['description']['identifier']='cavediamonds:cave_snap_'+surface
            surface_body['surface']=surface
            (pack/'features'/('cave_snap_'+surface+'.json')).write_text(json.dumps(surface_doc,indent=2)+'\n')
        feature('cave_snap_choice','minecraft:weighted_random_feature',{'features':[['cavediamonds:cave_snap_floor',1],['cavediamonds:cave_snap_ceiling',1],['cavediamonds:cave_snap_wall',1]]})
        if profile=='v12':
            rules=[('cave_rule',[-64,-48],1,None),('cave_deep_extra',[-64,-48],1,80),('cave_mid_rule',[-47,-1],1,None),('cave_high_rule',[0,4],1,5)]
        elif profile=='v13':
            rules=[('cave_rule',[-64,-33],1,None),('cave_mid_rule',[-32,-1],1,None),('cave_high_rule',[0,4],1,5)]
        elif profile=='v14':
            rules=[('cave_rule',[-64,-33],1,None),('cave_mid_rule',[-32,-1],1,80),('cave_high_rule',[0,4],1,5)]
        elif profile=='v15':
            rules=[('cave_rule',[-64,-33],1,None),('cave_mid_rule',[-32,-1],1,90),('cave_high_rule',[0,4],1,5)]
        elif profile=='v16':
            rules=[('cave_rule',[-64,-33],2,None),('cave_mid_rule',[-32,-1],1,None),('cave_high_rule',[0,4],1,0)]
        elif profile=='v17':
            rules=[('cave_rule',[-64,-33],1,None),('cave_mid_rule',[-32,-1],1,90),('cave_high_rule',[0,4],1,0)]
        elif profile=='v18':
            rules=[('cave_rule',[-64,-33],1,None),('cave_mid_rule',[-32,-1],1,90)]
        elif profile=='v19':
            rules=[('cave_rule',[-64,-33],1,None),('cave_deep_extra',[-64,-33],1,50),('cave_mid_rule',[-32,-1],1,90)]
        else:
            rules=[('cave_rule',[-64,-48],1,None),('cave_mid_rule',[-47,-1],1,None),('cave_high_rule',[0,4],1,5)] if profile in ('v10','v11') else [('cave_rule',[-64,-33],2,None),('cave_mid_rule',[-32,-1],1,None),('cave_high_rule',[0,4],1,30 if profile=='v7' else 10)]
        for name,extent,iterations,chance in rules:
            doc=json.loads(json.dumps(cave))
            body=doc['minecraft:feature_rules']
            body['description']={'identifier':'cavediamonds:'+name,'places_feature':'cavediamonds:cave_snap_choice'}
            body['distribution']['y']['extent']=extent
            body['distribution']['iterations']=iterations
            if chance is not None: body['distribution']['scatter_chance']=chance
            (pack/'feature_rules'/(name+'.json')).write_text(json.dumps(doc,indent=2)+'\n')
    buried_path=pack/'feature_rules/sparse_buried_rule.json'
    buried=json.loads(buried_path.read_text())
    buried['minecraft:feature_rules']['distribution']['y']['extent']=[-64,-32] if profile=='v1' else [-64,16]
    buried['minecraft:feature_rules']['distribution']['iterations']=1 if profile=='v1' else 3 if profile=='v19' else 2
    buried_path.write_text(json.dumps(buried,indent=2)+'\n')
    for name in ('scan_chunk','select_ore','thin_deepslate','thin_diamond','cave_snap_select') + (() if profile in ('v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19') else ('cave_snap_ceiling',)):
        (pack/'features'/(name+'.json')).unlink()
    manifest_path=pack/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    manifest['header']['name']=f'Cave Diamonds – Balance Test {profile} (nicht freigegeben)'
    manifest['header']['description']='Testpaket: keine Freigabe für Spielwelten oder Realms'
    manifest['header']['min_engine_version']=[1,26,60]
    manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    return pack

def read_reference(reference_path=REFERENCE):
    reference=json.loads(reference_path.read_text())
    if reference['server_version']!='1.26.61.1': raise ValueError('unexpected baseline server version')
    return reference

def scan_area(pack, result_dir, index, reference_path=REFERENCE):
    if not eula_accepted(ROOT/'.env'): raise RuntimeError('Explicit EULA=TRUE in .env required')
    reference=read_reference(reference_path)
    if not 0 <= index < len(reference['areas']): raise ValueError('invalid area index')
    area=reference['areas'][index]
    result_path=result_dir/f'area-{index:02d}.json'
    result_dir.mkdir(parents=True,exist_ok=True)
    if result_path.exists(): raise FileExistsError(f'refusing to overwrite {result_path}')
    candidate_hash=pack_digest(pack)
    reference_hash=hashlib.sha256(reference_path.read_bytes()).hexdigest()
    for path in result_dir.glob('area-*.json'):
        old=json.loads(path.read_text())
        if old.get('pack_sha256')!=candidate_hash or old.get('reference_sha256')!=reference_hash:
            raise ValueError(f'incompatible existing result: {path}')
    baseline_scan=json.loads((ROOT/area['scan_file']).read_text())
    n=area['chunks_per_side']; x=area['chunk_x']; z=area['chunk_z']; seed=area['seed']
    baseline=analyze(baseline_scan,x*16,z*16,n*16)
    print(f'Gebiet {index+1}/{len(reference["areas"])}: Seed {seed}, Chunk {x}/{z}',flush=True)
    world=run(seed,True,n,diagnose=True,pack_path=pack,chunk_x=x,chunk_z=z,height_probe=True)
    world_path=Path(world['world'])
    log=(world_path/'server.log').read_text(errors='replace')
    if pack_digest(pack)!=candidate_hash: raise RuntimeError('pack changed during scan')
    if hashlib.sha256(reference_path.read_bytes()).hexdigest()!=reference_hash: raise RuntimeError('reference changed during scan')
    if 'Version: 1.26.61.1' not in log: raise RuntimeError(f'wrong server version; inspect {world_path}')
    if '[ERROR] [Scripting]' in log or '[ERROR] [Json]' in log: raise RuntimeError(f'content error; inspect {world_path}')
    scan=json.loads((world_path/'ore_scan.json').read_text())
    candidate=analyze(scan,x*16,z*16,n*16)
    def contacts(data):
        return sum(count_tunnel_finds(data['ores'],n*16,-57,x*16,z*16).values())
    result={'index':index,'seed':seed,'chunk_x':x,'chunk_z':z,'chunks_per_side':n,
            'pack_sha256':candidate_hash,'reference_sha256':reference_hash,
            'reference_world_scan':area['scan_file'],'candidate_world':str(world_path.relative_to(ROOT)),
            'vanilla':baseline,'candidate':candidate,
            'tunnel_contacts':{'vanilla':contacts(baseline_scan),'candidate':contacts(scan)},
            'candidate_upper_diamonds_17_to_40':len(scan['upperDiamondOre'])}
    write_result_once(result_path,result)
    print('BALANCE_AREA '+json.dumps({'index':index,'result':str(result_path),
          'vanilla_air_groups':baseline['deposits']['air_adjacent'],'candidate_air_groups':candidate['deposits']['air_adjacent'],
          'vanilla_y57':baseline['y_minus57']['buried'],'candidate_y57':candidate['y_minus57']['buried'],
          'tunnel_contacts':result['tunnel_contacts']}),flush=True)

def summarize(result_dir, reference_path=REFERENCE):
    results=[json.loads(p.read_text()) for p in sorted(result_dir.glob('area-*.json'))]
    if not results: raise ValueError('no completed areas')
    if len({r.get('pack_sha256') for r in results})!=1 or not results[0].get('pack_sha256'):
        raise ValueError('mixed or missing candidate fingerprints')
    if len({r.get('reference_sha256') for r in results})!=1 or not results[0].get('reference_sha256'):
        raise ValueError('mixed or missing reference fingerprints')
    if results[0]['reference_sha256']!=hashlib.sha256(reference_path.read_bytes()).hexdigest():
        raise ValueError('results do not match the selected reference')
    def reports(key):
        return [{'seed':r['seed'],'chunk_x':r['chunk_x'],'chunk_z':r['chunk_z'],
                 'chunks_per_side':r['chunks_per_side'],**r[key]} for r in results]
    vanilla=aggregate(reports('vanilla')); candidate=aggregate(reports('candidate'))
    tunnel={key:sum(r['tunnel_contacts'][key] for r in results) for key in ('vanilla','candidate')}
    return {'areas':len(results),'expected_areas':len(read_reference(reference_path)['areas']),
            'pack_sha256':results[0]['pack_sha256'],'reference_sha256':results[0]['reference_sha256'],
            'indexes':[r['index'] for r in results],'vanilla':vanilla,'candidate':candidate,'tunnel_contacts':tunnel}

def verify_mining(pack, result_dir, index):
    if not eula_accepted(ROOT/'.env'): raise RuntimeError('Explicit EULA=TRUE in .env required')
    reference=read_reference()
    if not 0 <= index < len(reference['areas']): raise ValueError('invalid area index')
    area=reference['areas'][index]
    result_dir.mkdir(parents=True,exist_ok=True)
    result_path=result_dir/f'mining-{index:02d}.json'
    if result_path.exists(): raise FileExistsError(f'refusing to overwrite {result_path}')
    digest=pack_digest(pack)
    n=area['chunks_per_side']; x=area['chunk_x']; z=area['chunk_z']; seed=area['seed']
    print(f'Abbauprobe Gebiet {index+1}: Seed {seed}, Chunk {x}/{z}',flush=True)
    created=run(seed,True,n,diagnose=True,pack_path=pack,chunk_x=x,chunk_z=z,mine_one=True)
    data=Path(created['world'])
    before=json.loads((data/'ore_scan.json').read_text())
    mined=json.loads((data/'simulated_mine.json').read_text())
    run(seed,True,n,diagnose=True,pack_path=pack,chunk_x=x,chunk_z=z,restart_world=data)
    after=json.loads((data/'ore_scan_after_restart.json').read_text())
    if pack_digest(pack)!=digest: raise RuntimeError('pack changed during test')
    for log in ('server.log','server_after_restart.log'):
        if 'Version: 1.26.61.1' not in (data/log).read_text(errors='replace'): raise RuntimeError('unexpected server version')
    result={'index':index,'seed':seed,'chunk_x':x,'chunk_z':z,'pack_sha256':digest,
            'world':str(data.relative_to(ROOT)),'mined':mined,**evaluate_mining(before,after,mined),
            'note':'setblock air, not real player mining; non-modified chunks may regenerate'}
    write_result_once(result_path,result)
    print('MINING_VERIFICATION '+json.dumps(result),flush=True)

def trace_ores(pack, result_dir, index):
    if not eula_accepted(ROOT/'.env'): raise RuntimeError('Explicit EULA=TRUE in .env required')
    reference=read_reference()
    if not 0 <= index < len(reference['areas']): raise ValueError('invalid area index')
    area=reference['areas'][index]
    result_dir.mkdir(parents=True,exist_ok=True)
    result_path=result_dir/f'ore-trace-{index:02d}.json'
    if result_path.exists(): raise FileExistsError(f'refusing to overwrite {result_path}')
    digest=pack_digest(pack)
    n=area['chunks_per_side']; x=area['chunk_x']; z=area['chunk_z']; seed=area['seed']
    scans=[]; worlds=[]
    for addon in (False,False,True):
        print(f'Erzpositionsprobe Gebiet {index+1}: {len(scans)+1}/3',flush=True)
        created=run(seed,addon,n,diagnose=True,pack_path=pack if addon else None,chunk_x=x,chunk_z=z,ore_trace=True)
        world=Path(created['world']); log=(world/'server.log').read_text(errors='replace')
        if 'Version: 1.26.61.1' not in log or '[ERROR] [Scripting]' in log or '[ERROR] [Json]' in log:
            raise RuntimeError(f'server or content error; inspect {world}')
        scan=json.loads((world/'ore_scan.json').read_text())
        if not scan.get('oreTrace'): raise RuntimeError(f'empty ore trace; inspect {world}')
        scans.append(scan); worlds.append(str(world.relative_to(ROOT)))
    if pack_digest(pack)!=digest: raise RuntimeError('pack changed during test')
    result={'index':index,'seed':seed,'chunk_x':x,'chunk_z':z,'pack_sha256':digest,
            'worlds':worlds,'trace_counts':[len(s['oreTrace']) for s in scans],
            'vanilla_repeat':diff_ore_trace(scans[0],scans[1]),
            'candidate_vs_vanilla':diff_ore_trace(scans[0],scans[2]),
            'note':'Only selected ore types and Y=-64..16; position differences do not establish a direct cause.'}
    write_result_once(result_path,result)
    print('ORE_TRACE '+json.dumps(result),flush=True)

def probe_surfaces(pack, result_dir):
    if not eula_accepted(ROOT/'.env'): raise RuntimeError('Explicit EULA=TRUE in .env required')
    result_dir.mkdir(parents=True,exist_ok=True)
    result_path=result_dir/'surface-probes.json'
    if result_path.exists(): raise FileExistsError(f'refusing to overwrite {result_path}')
    digest=pack_digest(pack)
    created=run(42,True,2,pack_path=pack,probe_snap=True)
    world=Path(created['world']); log=(world/'server.log').read_text(errors='replace')
    if 'Version: 1.26.61.1' not in log or '[ERROR] [Scripting]' in log or '[ERROR] [Json]' in log:
        raise RuntimeError(f'server or content error; inspect {world}')
    if pack_digest(pack)!=digest: raise RuntimeError('pack changed during test')
    result={'pack_sha256':digest,'world':str(world.relative_to(ROOT)),
            'probes':json.loads((world/'snap_probes.json').read_text()),
            'note':'Controlled hollow box; successful placement does not prove natural generation or cave accessibility.'}
    write_result_once(result_path,result)
    print('SURFACE_PROBES '+json.dumps(result),flush=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    build=sub.add_parser('build'); build.add_argument('--output',type=Path,required=True); build.add_argument('--profile',choices=('v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19'),default='v1')
    scan=sub.add_parser('scan'); scan.add_argument('--pack',type=Path,required=True); scan.add_argument('--results',type=Path,required=True); scan.add_argument('--index',type=int,required=True); scan.add_argument('--reference',type=Path,default=REFERENCE)
    summary=sub.add_parser('summarize'); summary.add_argument('--results',type=Path,required=True); summary.add_argument('--reference',type=Path,default=REFERENCE)
    verify=sub.add_parser('verify-mining'); verify.add_argument('--pack',type=Path,required=True); verify.add_argument('--results',type=Path,required=True); verify.add_argument('--index',type=int,required=True)
    trace=sub.add_parser('trace-ores'); trace.add_argument('--pack',type=Path,required=True); trace.add_argument('--results',type=Path,required=True); trace.add_argument('--index',type=int,required=True)
    probe=sub.add_parser('probe-surfaces'); probe.add_argument('--pack',type=Path,required=True); probe.add_argument('--results',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='build': print(create_candidate(ROOT/'prototype/behavior_pack',args.output,profile=args.profile))
    elif args.command=='scan': scan_area(args.pack.resolve(),args.results,args.index,args.reference)
    elif args.command=='verify-mining': verify_mining(args.pack.resolve(),args.results,args.index)
    elif args.command=='trace-ores': trace_ores(args.pack.resolve(),args.results,args.index)
    elif args.command=='probe-surfaces': probe_surfaces(args.pack.resolve(),args.results)
    else: print(json.dumps(summarize(args.results,args.reference),indent=2))

if __name__=='__main__': main()
